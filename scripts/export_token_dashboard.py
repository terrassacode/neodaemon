#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

WORKSPACE = Path("/openclaw/workspace/main")
SOURCE_PATH = WORKSPACE / "logs" / "resource_usage.jsonl"
OUTPUT_PATH = WORKSPACE / "dashboard-v2" / "data" / "token_dashboard.json"
MODEL = "ChatGPT 5.5"


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def safe_int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def estimate_tokens(chars: int) -> int:
    return round(chars / 4)


def load_events() -> list[dict[str, Any]]:
    if not SOURCE_PATH.exists():
        return []

    events = []
    for line in SOURCE_PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(item, dict):
            events.append(item)
    return events


def event_tokens(event: dict[str, Any]) -> tuple[int, int, int]:
    input_tokens = estimate_tokens(safe_int(event.get("input_chars")))
    output_tokens = estimate_tokens(safe_int(event.get("output_chars")))
    return input_tokens, output_tokens, input_tokens + output_tokens


def add_group(groups: dict[str, dict[str, Any]], key: str, event: dict[str, Any]) -> None:
    input_tokens, output_tokens, total_tokens = event_tokens(event)

    group = groups.setdefault(key, {
        "events": 0,
        "input_tokens_estimated": 0,
        "output_tokens_estimated": 0,
        "total_tokens_estimated": 0,
        "last_action": "",
        "last_timestamp": "",
        "results": set(),
    })

    group["events"] += 1
    group["input_tokens_estimated"] += input_tokens
    group["output_tokens_estimated"] += output_tokens
    group["total_tokens_estimated"] += total_tokens
    group["results"].add(str(event.get("result") or "sin resultado"))

    timestamp = str(event.get("timestamp") or "")
    if timestamp >= group["last_timestamp"]:
        group["last_timestamp"] = timestamp
        group["last_action"] = str(event.get("action") or event.get("flow") or "sin acción")


def serialize_group(key_name: str, key: str, group: dict[str, Any]) -> dict[str, Any]:
    return {
        key_name: key,
        "events": group["events"],
        "input_tokens_estimated": group["input_tokens_estimated"],
        "output_tokens_estimated": group["output_tokens_estimated"],
        "total_tokens_estimated": group["total_tokens_estimated"],
        "last_action": group["last_action"],
        "results": sorted(group["results"]),
    }


def build_payload() -> dict[str, Any]:
    events = load_events()

    totals = {
        "events": len(events),
        "actions_count": len(events),
        "interactions_count": 0,
        "responses_tokens_estimated": 0,
        "events_without_interaction_id_count": 0,
        "input_tokens_estimated": 0,
        "output_tokens_estimated": 0,
        "total_tokens_estimated": 0,
    }

    tokens_by_day = defaultdict(int)
    tokens_by_hour = defaultdict(int)
    interactions: dict[str, dict[str, Any]] = {}
    interaction_ids: set[str] = set()
    actions: dict[str, dict[str, Any]] = {}
    without_interaction: dict[str, dict[str, Any]] = {}

    without_totals = {
        "events": 0,
        "input_tokens_estimated": 0,
        "output_tokens_estimated": 0,
        "total_tokens_estimated": 0,
    }

    for event in events:
        input_tokens, output_tokens, total_tokens = event_tokens(event)
        totals["input_tokens_estimated"] += input_tokens
        totals["output_tokens_estimated"] += output_tokens
        totals["responses_tokens_estimated"] += output_tokens
        totals["total_tokens_estimated"] += total_tokens

        timestamp = str(event.get("timestamp") or "")
        day = timestamp[:10] if len(timestamp) >= 10 else "sin_fecha"
        hour = timestamp[:13] if len(timestamp) >= 13 else "sin_hora"

        tokens_by_day[day] += total_tokens
        tokens_by_hour[hour] += total_tokens

        action = str(event.get("action") or event.get("flow") or "sin acción")
        add_group(actions, action, event)

        interaction_id = str(event.get("interaction_id") or "").strip()
        if interaction_id:
            interaction_ids.add(interaction_id)
            add_group(interactions, interaction_id, event)
        else:
            totals["events_without_interaction_id_count"] += 1
            without_totals["events"] += 1
            without_totals["input_tokens_estimated"] += input_tokens
            without_totals["output_tokens_estimated"] += output_tokens
            without_totals["total_tokens_estimated"] += total_tokens
            add_group(without_interaction, action, event)

    totals["interactions_count"] = len(interaction_ids)

    top_interactions = [
        serialize_group("interaction_id", key, group)
        for key, group in sorted(
            interactions.items(),
            key=lambda item: item[1]["total_tokens_estimated"],
            reverse=True,
        )[:10]
    ]

    top_actions = [
        serialize_group("action", key, group)
        for key, group in sorted(
            actions.items(),
            key=lambda item: item[1]["total_tokens_estimated"],
            reverse=True,
        )[:10]
    ]

    top_without = [
        serialize_group("action", key, group)
        for key, group in sorted(
            without_interaction.items(),
            key=lambda item: item[1]["total_tokens_estimated"],
            reverse=True,
        )[:10]
    ]

    return {
        "generated_at": now_iso(),
        "model": MODEL,
        "source": "logs/resource_usage.jsonl",
        "estimation": {
            "input_tokens": "input_chars / 4",
            "output_tokens": "output_chars / 4",
            "total_tokens": "input_tokens + output_tokens",
        },
        "totals": totals,
        "tokens_by_day": dict(sorted(tokens_by_day.items())),
        "tokens_by_hour": dict(sorted(tokens_by_hour.items())),
        "top_interactions": top_interactions,
        "top_actions": top_actions,
        "events_without_interaction_id": {
            **without_totals,
            "top_actions": top_without,
        },
    }


def export() -> dict[str, Any]:
    payload = build_payload()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    payload = export()
    print(json.dumps({
        "status": "ok",
        "output": str(OUTPUT_PATH),
        "events": payload["totals"]["events"],
        "total_tokens_estimated": payload["totals"]["total_tokens_estimated"],
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
