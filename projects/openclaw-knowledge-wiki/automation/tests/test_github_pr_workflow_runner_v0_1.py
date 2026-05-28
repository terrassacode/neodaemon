#!/usr/bin/env python3
"""
Minimal tests for github_pr_workflow_runner.py v0.1.

Constraints:
- stdlib only
- no Git execution
- no repo clean access
- no branches
- no copy/commit/push/PR/merge
- no run_state creation
- no approvals creation
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RUNNER_PATH = PROJECT_ROOT / "automation" / "github_pr_workflow_runner.py"
POLICY_PATH = PROJECT_ROOT / "automation" / "policies" / "github_pr_workflow.policy.yml"


def load_runner():
    spec = importlib.util.spec_from_file_location("github_pr_workflow_runner", RUNNER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load runner module")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def capture_main(module, argv):
    stdout = io.StringIO()
    with contextlib.redirect_stdout(stdout):
        code = module.main(argv)

    payload = json.loads(stdout.getvalue())
    return code, payload


def valid_policy_text():
    return POLICY_PATH.read_text(encoding="utf-8")


def remove_not_implemented_command(policy_text: str, command: str) -> str:
    lines = policy_text.splitlines()
    output = []
    in_block = False
    block_indent = None
    removed = False

    for line in lines:
        stripped = line.strip()

        if stripped == "not_implemented_commands:":
            in_block = True
            block_indent = len(line) - len(line.lstrip(" "))
            output.append(line)
            continue

        if in_block:
            indent = len(line) - len(line.lstrip(" "))

            if stripped and indent <= block_indent and not stripped.startswith("- "):
                in_block = False

            if in_block and stripped == f"- {command}":
                removed = True
                continue

        output.append(line)

    if not removed:
        raise AssertionError(f"command not found in not_implemented_commands: {command}")

    return "\n".join(output) + "\n"


class GitHubPRWorkflowRunnerV01Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.runner = load_runner()

    def test_valid_policy_plan_docs_low_risk_pass(self):
        code, payload = capture_main(
            self.runner,
            [
                "plan",
                "--policy",
                str(POLICY_PATH),
                "--change-class",
                "DOCS_LOW_RISK",
            ],
        )

        self.assertEqual(code, 0)
        self.assertEqual(payload["status"], "PASS")
        self.assertIs(payload["safe_to_execute"], False)

    def test_valid_policy_check_docs_low_risk_pass(self):
        code, payload = capture_main(
            self.runner,
            [
                "check",
                "--policy",
                str(POLICY_PATH),
                "--change-class",
                "DOCS_LOW_RISK",
            ],
        )

        self.assertEqual(code, 0)
        self.assertEqual(payload["status"], "PASS")
        self.assertIs(payload["safe_to_execute"], False)

    def test_change_class_code_blocks(self):
        code, payload = capture_main(
            self.runner,
            [
                "plan",
                "--policy",
                str(POLICY_PATH),
                "--change-class",
                "CODE",
            ],
        )

        self.assertNotEqual(code, 0)
        self.assertEqual(payload["status"], "BLOCK")
        self.assertIs(payload["safe_to_execute"], False)

    def test_auto_merge_enabled_true_blocks(self):
        text = valid_policy_text().replace("enabled: false", "enabled: true", 1)

        with tempfile.TemporaryDirectory() as tmp:
            policy = Path(tmp) / "policy.yml"
            policy.write_text(text, encoding="utf-8")

            code, payload = capture_main(
                self.runner,
                [
                    "check",
                    "--policy",
                    str(policy),
                    "--change-class",
                    "DOCS_LOW_RISK",
                ],
            )

        self.assertNotEqual(code, 0)
        self.assertEqual(payload["status"], "BLOCK")
        self.assertIs(payload["safe_to_execute"], False)

    def test_missing_merge_in_not_implemented_blocks(self):
        text = remove_not_implemented_command(valid_policy_text(), "merge")

        with tempfile.TemporaryDirectory() as tmp:
            policy = Path(tmp) / "policy.yml"
            policy.write_text(text, encoding="utf-8")

            code, payload = capture_main(
                self.runner,
                [
                    "check",
                    "--policy",
                    str(policy),
                    "--change-class",
                    "DOCS_LOW_RISK",
                ],
            )

        self.assertNotEqual(code, 0)
        self.assertEqual(payload["status"], "BLOCK")
        self.assertIs(payload["safe_to_execute"], False)

    def test_missing_policy_blocks(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "missing.yml"

            code, payload = capture_main(
                self.runner,
                [
                    "check",
                    "--policy",
                    str(missing),
                    "--change-class",
                    "DOCS_LOW_RISK",
                ],
            )

        self.assertEqual(code, 2)
        self.assertEqual(payload["status"], "BLOCK")
        self.assertIs(payload["safe_to_execute"], False)

    def test_unsupported_command_copy_fails_argparse(self):
        stderr = io.StringIO()

        with self.assertRaises(SystemExit) as ctx:
            with contextlib.redirect_stderr(stderr):
                self.runner.main(
                    [
                        "copy",
                        "--policy",
                        str(POLICY_PATH),
                        "--change-class",
                        "DOCS_LOW_RISK",
                    ]
                )

        self.assertNotEqual(ctx.exception.code, 0)

    def test_runner_contains_no_subprocess(self):
        text = RUNNER_PATH.read_text(encoding="utf-8")
        self.assertNotIn("subprocess", text)

    def test_runner_contains_no_os_system(self):
        text = RUNNER_PATH.read_text(encoding="utf-8")
        self.assertNotIn("os.system", text)

    def test_runner_contains_no_git_push(self):
        text = RUNNER_PATH.read_text(encoding="utf-8")
        self.assertNotIn("git push", text)

    def test_runner_contains_no_gh_pr_create(self):
        text = RUNNER_PATH.read_text(encoding="utf-8")
        self.assertNotIn("gh pr create", text)

    def test_runner_does_not_create_runtime_dirs(self):
        text = RUNNER_PATH.read_text(encoding="utf-8")

        self.assertNotIn("mkdir", text)
        self.assertNotIn("run_state.mkdir", text)
        self.assertNotIn("approvals.mkdir", text)

    def test_runner_never_contains_safe_to_execute_true_literal(self):
        text = RUNNER_PATH.read_text(encoding="utf-8")

        self.assertNotIn('"safe_to_execute": True', text)
        self.assertNotIn("'safe_to_execute': True", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
