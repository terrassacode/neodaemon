#!/usr/bin/env python3
"""Validate proposed actions against Neodaemon project isolation policy.

This script is advisory only. It does not execute actions.
It returns a JSON decision for review by Neodaemon MAIN / TASK_VALIDATOR.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

VALID_TYPES = {"read", "write", "execute", "git", "network", "service"}
VALID_RISKS = {"low", "medium", "high"}

PROJECTS_ROOT = Path("/openclaw/workspace/main/projects").resolve()
MAIN_ROOT = Path("/openclaw/workspace/main").resolve()
GLOBAL_SCRIPTS = Path("/openclaw/workspace/main/scripts").resolve()

FORBIDDEN_PATHS = [
    Path("/openclaw/core").resolve(),
    Path("/openclaw/workspace/main/scripts").resolve(),
    Path("/openclaw/workspace/main/systemd").resolve(),
    Path("/openclaw/workspace/main/rag_store").resolve(),
    Path("/openclaw/workspace/main/memory").resolve(),
    Path("/openclaw/workspace/main/.openclaw").resolve(),
    Path("/openclaw/workspace/main/context_repo").resolve(),
    Path("/openclaw/workspace/main/dashboard-v2").resolve(),
    Path("/openclaw/workspace/main/logs").resolve(),
    Path("/openclaw/workspace/main/backups").resolve(),
    Path("/openclaw/workspace/main/briefings").resolve(),
    Path("/openclaw/workspace/git_clean").resolve(),
    Path("/openclaw/.env").resolve(),
    Path("/home/openclaw/.openclaw").resolve(),
]


def is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def normalize(path: str) -> Path:
    return Path(path).resolve()


def is_forbidden(path: Path) -> bool:
    return any(path == blocked or is_relative_to(path, blocked) for blocked in FORBIDDEN_PATHS)


def set_decision(result: dict[str, Any], decision: str, reason: str, rule: str) -> None:
    priority = {"ALLOW": 0, "NEEDS_APPROVAL": 1, "BLOCK": 2}
    if priority[decision] > priority[result["decision"]]:
        result["decision"] = decision
    result["reasons"].append(reason)
    result["matched_rules"].append(rule)


def validate(action: str, path: str, action_type: str, risk: str) -> dict[str, Any]:
    action = str(action or "")
    path = str(path or "")
    action_type = str(action_type or "").lower()
    risk = str(risk or "").lower()
    action_lc = action.lower()

    result: dict[str, Any] = {
        "decision": "ALLOW",
        "risk": risk,
        "normalized_path": None,
        "reasons": [],
        "matched_rules": [],
        "requires_critical_analysis": risk in {"medium", "high"},
    }

    if action_type not in VALID_TYPES:
        set_decision(result, "BLOCK", "invalid action type", "input_validation:invalid_type")
        return result

    if risk not in VALID_RISKS:
        set_decision(result, "BLOCK", "invalid risk", "input_validation:invalid_risk")
        result["requires_critical_analysis"] = False
        return result

    if risk in {"medium", "high"}:
        result["matched_rules"].append("skeptical_mode:risk_override")
        result["reasons"].append("risk medium/high requires critical analysis")

    if action_type in {"read", "write", "execute"} and not path:
        set_decision(
            result,
            "BLOCK",
            "path is required for read/write/execute actions",
            "input_validation:path_required",
        )
        return result

    normalized: Path | None = None
    if action_type in {"read", "write", "execute"}:
        normalized = normalize(path)
        result["normalized_path"] = str(normalized)
    elif action_type in {"git", "network", "service"} and path:
        normalized = normalize(path)
        result["normalized_path"] = str(normalized)

    if action_type == "write" and normalized is not None:
        if is_forbidden(normalized):
            set_decision(
                result,
                "BLOCK",
                "write target is inside forbidden path",
                "project_isolation:write_forbidden_path",
            )
        elif not is_relative_to(normalized, PROJECTS_ROOT):
            set_decision(
                result,
                "BLOCK",
                "path escapes project boundary",
                "project_isolation:write_outside_projects_blocked",
            )

    if action_type == "execute" and normalized is not None:
        if is_relative_to(normalized, GLOBAL_SCRIPTS):
            set_decision(
                result,
                "BLOCK",
                "projects cannot execute global scripts",
                "project_isolation:execute_global_script_blocked",
            )
        if normalized.name in {"ru_event.sh", "ru_interaction.sh"}:
            set_decision(
                result,
                "BLOCK",
                "projects cannot invoke Resource Usage global wrappers",
                "project_isolation:ru_wrappers_blocked",
            )

    if action_type == "git":
        if "git push" in action_lc:
            set_decision(
                result,
                "NEEDS_APPROVAL",
                "git push requires explicit approval",
                "git:push_requires_approval",
            )

        if "git add ." in action_lc:
            if normalized is not None and (normalized == MAIN_ROOT or is_relative_to(normalized, MAIN_ROOT)):
                set_decision(
                    result,
                    "BLOCK",
                    "git add . from main workspace is forbidden",
                    "git:add_dot_main_blocked",
                )
            elif "/openclaw/workspace/main" in action_lc:
                set_decision(
                    result,
                    "BLOCK",
                    "git add . from main workspace is forbidden",
                    "git:add_dot_main_blocked",
                )

    if action_type == "service":
        if any(word in action_lc for word in ["systemd", "gateway"]):
            set_decision(
                result,
                "BLOCK",
                "service/gateway operations are blocked by policy",
                "services:systemd_gateway_blocked",
            )

    if action_type == "network":
        if any(word in action_lc for word in ["gmail", "telegram", "api", "publicar", "post"]):
            set_decision(
                result,
                "NEEDS_APPROVAL",
                "external integration requires explicit approval",
                "network:external_requires_approval",
            )

    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate an action against Neodaemon policy")
    parser.add_argument("--action", required=True)
    parser.add_argument("--path", default="")
    parser.add_argument("--type", required=True)
    parser.add_argument("--risk", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = validate(args.action, args.path, args.type, args.risk)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
