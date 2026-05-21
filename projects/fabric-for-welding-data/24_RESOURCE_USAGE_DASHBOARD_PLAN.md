# 24_RESOURCE_USAGE_DASHBOARD_PLAN.md

Status: design only  
Scope: estimated resource usage logging for future dashboard  
Version: v1.0

---

## 1. Purpose

Define a minimal design to log estimated resource consumption per Neodaemon action.

The goal is to detect which flows consume more context, tokens or operational budget before implementing any dashboard changes.

This document is specification only.

No code is implemented here.

---

## 2. Log path

Canonical future log path:

```text
/openclaw/workspace/main/logs/resource_usage.jsonl
```

Format:

```text
JSON Lines, one action/event per line
```

---

## 3. Token estimation formula

Approximate formula:

```text
estimated_tokens = caracteres / 4
```

Rules:

- Count visible text characters from relevant input/output payloads.
- Use integer rounding when storing the value.
- This is an estimate, not provider billing truth.
- Use it only for trend detection and flow comparison.

---

## 4. Minimal JSONL fields

Each JSONL event should contain at least:

```json
{
  "timestamp": "2026-05-21T00:00:00+02:00",
  "session": "main",
  "agent": "Neodaemon",
  "flow": "VALIDAR_LOW_SCOPE | TASK_VALIDATOR | ASSISTED_EXECUTION | POST_ACTION_REVIEW | briefing | rag_debug | other",
  "action": "short action name",
  "target": "path or logical target",
  "input_chars": 0,
  "output_chars": 0,
  "total_chars": 0,
  "estimated_tokens": 0,
  "result": "ok | partial | blocked | error",
  "usage_limit": false,
  "usage_limit_reason": ""
}
```

Optional future fields:

```json
{
  "model": "",
  "tool_calls": 0,
  "files_read": 0,
  "files_written": 0,
  "duration_ms": 0,
  "risk_score": null,
  "error_mode": false
}
```

---

## 5. Dashboard KPIs

Initial KPIs for a future dashboard:

- total estimated tokens per day;
- estimated tokens by flow;
- top 10 most expensive actions;
- average estimated tokens per action;
- count of actions by result: `ok`, `partial`, `blocked`, `error`;
- count of `usage_limit = true` events;
- estimated tokens spent on blocked/error actions;
- trend over last 7 days;
- ratio of validation overhead vs execution actions.

---

## 6. usage_limit rule

Set:

```json
"usage_limit": true
```

when one or more conditions apply:

- estimated tokens exceed a future configured per-action threshold;
- action produces excessive output compared with its purpose;
- repeated validation loops inflate cost;
- context is too broad for the requested task;
- `git diff` or logs are too large;
- RAG/debug output is broader than needed;
- action should be split into smaller scoped steps.

When `usage_limit = true`, `usage_limit_reason` must explain why.

Example:

```json
{
  "usage_limit": true,
  "usage_limit_reason": "git status/diff output too broad for target scope"
}
```

---

## 7. Non-goals

This plan does not implement:

- code changes;
- dashboard changes;
- runtime hooks;
- RAG changes;
- token provider billing integration;
- gateway changes;
- model changes;
- automated enforcement.

---

## 8. Future implementation notes

A future implementation should be low-scope and phased:

1. create append-only JSONL writer;
2. log only manual/MAIN actions first;
3. add dashboard read-only summary;
4. add thresholds for `usage_limit`;
5. review with Albert before automation.

Each phase requires separate TASK_VALIDATOR and explicit authorization.
