#!/usr/bin/env python3
"""
github_pr_workflow_runner.py v0.1

Read-only policy runner for github-pr-workflow.

v0.1 supports only:
- plan
- check

It must not:
- copy files
- create branches
- run Git commands
- create run_state
- create approvals
- commit
- push
- create PRs
- merge
- modify files

All outputs keep safe_to_execute=false.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


EXPECTED_WORKSPACE_ROOT = "/openclaw/workspace/main"
EXPECTED_REPO_ROOT = "/openclaw/workspace/git_clean/neodaemon_repo"
EXPECTED_RUN_STATE_DIR = "projects/openclaw-knowledge-wiki/automation/run_state"
EXPECTED_CHANGE_CLASS = "DOCS_LOW_RISK"
EXPECTED_IMPLEMENTED_COMMANDS = ["plan", "check"]
EXPECTED_NOT_IMPLEMENTED = ["copy", "commit", "push", "pr", "merge"]


def parse_scalar(value: str):
    value = value.strip()
    if value == "true":
        return True
    if value == "false":
        return False
    if value == "null":
        return None

    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]

    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]

    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return value


def minimal_yaml_parse(text: str) -> dict:
    root = {}
    stack = [(-1, root)]

    list_keys = {
        "allowed_paths",
        "forbidden_paths",
        "allowed_extensions",
        "allowed_encodings",
        "pr_labels",
        "implemented_commands",
        "not_implemented_commands",
        "deny",
    }

    for raw_line in text.splitlines():
        if not raw_line.strip():
            continue

        stripped = raw_line.strip()
        if stripped.startswith("#"):
            continue

        indent = len(raw_line) - len(raw_line.lstrip(" "))

        while stack and indent <= stack[-1][0]:
            stack.pop()

        parent = stack[-1][1]

        if stripped.startswith("- "):
            item = parse_scalar(stripped[2:])
            if not isinstance(parent, list):
                raise ValueError("list item without list parent")
            parent.append(item)
            continue

        if ":" not in stripped:
            raise ValueError(f"unsupported YAML line: {stripped}")

        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip()

        if value == "":
            new_obj = [] if key in list_keys else {}
            parent[key] = new_obj
            stack.append((indent, new_obj))
        else:
            parent[key] = parse_scalar(value)

    return root


def load_policy(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    return minimal_yaml_parse(text)


def block(reason: str, details: dict | None = None) -> dict:
    return {
        "status": "BLOCK",
        "safe_to_execute": False,
        "reason": reason,
        "details": details or {},
    }


def pass_result(command: str, policy_path: str, change_class: str, details: dict) -> dict:
    return {
        "status": "PASS",
        "command": command,
        "safe_to_execute": False,
        "policy": policy_path,
        "change_class": change_class,
        "details": details,
    }


def require(condition: bool, reason: str):
    if not condition:
        raise ValueError(reason)


def validate_policy(policy: dict, change_class: str) -> dict:
    require(policy.get("version") == 0.1, "policy.version must be 0.1")
    require(policy.get("default_safe_to_execute") is False, "default_safe_to_execute must be false")

    paths = policy.get("paths")
    require(isinstance(paths, dict), "paths must exist")

    workspace_root = paths.get("workspace_root")
    repo_root = paths.get("repo_root")
    run_state_dir = paths.get("run_state_dir")

    require(workspace_root == EXPECTED_WORKSPACE_ROOT, "unexpected workspace_root")
    require(repo_root == EXPECTED_REPO_ROOT, "unexpected repo_root")
    require(run_state_dir == EXPECTED_RUN_STATE_DIR, "unexpected run_state_dir")

    change_classes = policy.get("change_classes")
    require(isinstance(change_classes, dict), "change_classes must exist")
    require(change_class == EXPECTED_CHANGE_CLASS, "unsupported change_class")
    require(change_class in change_classes, "DOCS_LOW_RISK missing")

    cls = change_classes[change_class]
    require(isinstance(cls, dict), "DOCS_LOW_RISK must be mapping")

    allowed_paths = cls.get("allowed_paths")
    forbidden_paths = cls.get("forbidden_paths")
    require(isinstance(allowed_paths, list) and allowed_paths, "allowed_paths must be non-empty list")
    require(isinstance(forbidden_paths, list) and forbidden_paths, "forbidden_paths must be non-empty list")

    require(cls.get("reject_symlinks") is True, "reject_symlinks must be true")
    require(cls.get("reject_binary") is True, "reject_binary must be true")
    require(cls.get("reject_path_traversal") is True, "reject_path_traversal must be true")
    require(cls.get("require_realpath_inside_allowlist") is True, "require_realpath_inside_allowlist must be true")
    require(cls.get("require_snapshot_before_copy") is True, "require_snapshot_before_copy must be true")
    require(cls.get("require_append_only_log") is True, "require_append_only_log must be true")
    require(cls.get("require_index_reference") is True, "require_index_reference must be true")
    require(cls.get("require_secret_scan") is True, "require_secret_scan must be true")
    require(cls.get("require_diff_policy") is True, "require_diff_policy must be true")
    require(cls.get("require_post_copy_revalidation") is True, "require_post_copy_revalidation must be true")
    require(cls.get("allow_auto_merge") is False, "allow_auto_merge must be false")

    runner = policy.get("runner_v0_1")
    require(isinstance(runner, dict), "runner_v0_1 must exist")

    implemented = runner.get("implemented_commands")
    not_implemented = runner.get("not_implemented_commands")

    require(implemented == EXPECTED_IMPLEMENTED_COMMANDS, "runner_v0_1 implemented_commands must be plan/check")
    require(isinstance(not_implemented, list), "not_implemented_commands must be list")

    missing = [cmd for cmd in EXPECTED_NOT_IMPLEMENTED if cmd not in not_implemented]
    require(not missing, f"not_implemented_commands missing: {missing}")

    github = policy.get("github")
    require(isinstance(github, dict), "github must exist")
    auto_merge = github.get("auto_merge")
    require(isinstance(auto_merge, dict), "github.auto_merge must exist")
    require(auto_merge.get("enabled") is False, "auto_merge.enabled must be false")

    return {
        "workspace_root": workspace_root,
        "repo_root": repo_root,
        "run_state_dir": run_state_dir,
        "allowed_paths": allowed_paths,
        "forbidden_paths": forbidden_paths,
        "implemented_commands": implemented,
        "not_implemented_commands": not_implemented,
        "auto_merge_enabled": auto_merge.get("enabled"),
        "allow_auto_merge": cls.get("allow_auto_merge"),
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read-only github PR workflow policy runner v0.1"
    )
    parser.add_argument("command", choices=["plan", "check"])
    parser.add_argument("--policy", required=True)
    parser.add_argument("--change-class", required=True)
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    policy_path = Path(args.policy)

    if not policy_path.exists():
        print(json.dumps(block("policy file does not exist", {"policy": args.policy}), indent=2))
        return 2

    try:
        policy = load_policy(policy_path)
        details = validate_policy(policy, args.change_class)
    except Exception as exc:
        print(json.dumps(block(str(exc), {"policy": args.policy}), indent=2))
        return 1

    payload = pass_result(args.command, args.policy, args.change_class, details)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
