# 26_OPERATIONAL_LOGGING_SYSTEM_PLAN.md

Status: design only  
Scope: operational logging architecture for OpenClaw MAIN  
Version: v1.0

---

## 1. Purpose

Design a structured, useful and queryable logging system for OpenClaw MAIN.

Goal:

```text
answer clearly: what happened, when, where, with what result, and what should happen next.
```

This document is a plan only.

No scripts, dashboard, runtime, services, RAG or systemd units are modified by this document.

---

## 2. Current log state

Current operational signals are split across several places.

### 2.1 systemd / journalctl

Source:

```text
journalctl --user -u <unit>
```

Known relevant units include:

```text
openclaw-resource-usage-export.timer
openclaw-resource-usage-export.service
openclaw-dashboard-web.service
openclaw-dashboard-html.service
openclaw-daily-briefing.service
openclaw-operational-alerts.service
openclaw-rag-v2.service
```

Role:

- raw service output;
- process failures;
- restarts;
- Python/bash errors;
- runtime-level signals.

Limitations:

- not normalized;
- not easy for non-technical review;
- requires host access;
- can include noisy HTTP lines;
- not always available from assistant sessions.

### 2.2 `alerts/alert.txt`

Source:

```text
/openclaw/workspace/main/alerts/alert.txt
```

Produced by:

```text
/openclaw/workspace/main/scripts/check_operational_alerts.sh
```

Role:

- simple text alert summary;
- current 2-hour operational window;
- groups signals by type and subsystem.

Limitations:

- plain text;
- overwritten by latest alert run;
- difficult to query historically;
- weak structure for dashboard and automation;
- may lose event-level detail.

### 2.3 `logs/resource_usage.jsonl`

Source:

```text
/openclaw/workspace/main/logs/resource_usage.jsonl
```

Role:

- append-only action/resource usage events;
- MAIN action counting;
- estimated token/activity tracking;
- source for Resource Usage dashboard export.

Limitations:

- focused on MAIN actions, not all system events;
- not a full operational timeline;
- does not include journal/service context;
- manual/semi-manual discipline still required.

### 2.4 `dashboard-v2/data/daily_summary.json`

Source:

```text
/openclaw/workspace/main/dashboard-v2/data/daily_summary.json
```

Role:

- human-readable daily summary data;
- non-technical status interpretation;
- source for daily Telegram summary.

Limitations:

- summary-level, not event-level;
- can be reset after send;
- not suitable as canonical event history;
- should not be used as raw evidence.

---

## 3. Current problems

### 3.1 Separate sources

Operational information is distributed across:

- systemd journal;
- alert text files;
- Resource Usage JSONL;
- dashboard JSON;
- daily summary JSON.

There is no single canonical timeline.

### 3.2 `alert.txt` is plain text

`alert.txt` is readable but not ideal for structured queries.

Problems:

- hard to count exact event types;
- hard to preserve history;
- hard to distinguish summary from evidence;
- fragile parsing in dashboard logic.

### 3.3 Missing consolidated timeline

There is no structured append-only file that answers:

```text
what happened and when?
```

This makes correlation harder between:

- MAIN actions;
- alerts;
- service events;
- daily summary send/reset;
- dashboard exports.

### 3.4 Difficult incident review

Today, answering a basic operational question often requires checking several files manually.

Examples:

```text
Why did the dashboard say Restarts/fallos: 1?
When was the last successful daily summary sent?
Which MAIN action happened before the alert?
Was a blocked action followed by a fix?
```

---

## 4. Proposed logging layers

The logging system should be layered, not monolithic.

```text
raw logs -> structured event logs -> alerts logs -> consolidated timeline -> human daily summary
```

### 4.1 Layer 1 — raw logs

Purpose:

```text
preserve original technical evidence.
```

Sources:

- `journalctl --user`;
- service stdout/stderr;
- script output;
- existing log files.

Rules:

- do not rewrite raw logs;
- do not expose secrets;
- use raw logs for diagnosis, not dashboard truth directly.

### 4.2 Layer 2 — structured event logs

Purpose:

```text
convert important events into append-only machine-readable records.
```

Candidate files:

```text
/openclaw/workspace/main/logs/resource_usage.jsonl
/openclaw/workspace/main/logs/operational_events.log
```

Future preferred file:

```text
/openclaw/workspace/main/logs/operational_timeline.jsonl
```

Role:

- canonical structured timeline;
- one event per line;
- stable schema;
- easy to query, aggregate and summarize.

### 4.3 Layer 3 — alerts logs

Purpose:

```text
record detected abnormal conditions without losing detail.
```

Examples:

- restart detected;
- repeated failures;
- BrokenPipeError above threshold;
- missing daily summary;
- export failure;
- blocked MAIN action.

Recommended output:

- keep `alerts/alert.txt` for human latest-state view;
- add structured alert events into `operational_timeline.jsonl` later.

### 4.4 Layer 4 — consolidated timeline

Purpose:

```text
provide one append-only chronological source for operational review.
```

Recommended canonical file:

```text
/openclaw/workspace/main/logs/operational_timeline.jsonl
```

It should include:

- MAIN actions;
- validation outcomes;
- dashboard exports;
- alert detections;
- daily summary send/reset;
- service checks when explicitly authorized;
- blocked/error events.

It should not include:

- tokens;
- prompts with sensitive content;
- `.env` values;
- full private messages;
- large raw stack traces unless sanitized.

### 4.5 Layer 5 — human daily summary

Purpose:

```text
produce a short non-technical daily status from structured data.
```

Source should be structured logs and metrics, not narrative invention.

Output examples:

```text
Se registraron 6 acciones.
5 acciones terminaron correctamente.
Hay 2 reinicios o fallos recientes.
```

Rules:

- no storytelling;
- no invented context;
- short direct phrases;
- reset only after successful send if configured.

---

## 5. Recommended JSONL schema

Recommended canonical timeline format:

```text
/openclaw/workspace/main/logs/operational_timeline.jsonl
```

Each line should be one JSON object.

Required fields:

```json
{
  "timestamp": "2026-05-22T09:48:00+02:00",
  "source": "MAIN | resource_usage | alerts | daily_summary | systemd | dashboard | rag_paused | other",
  "type": "action | validation | alert | summary | service | export | blocked | error",
  "severity": "info | warning | error | critical",
  "action": "short_action_name",
  "target": "path-or-component",
  "result": "ok | partial | blocked | error | unknown",
  "message": "short sanitized message",
  "next_step": "short next step or empty"
}
```

Field meaning:

- `timestamp`: ISO timestamp with timezone;
- `source`: subsystem or logical origin;
- `type`: event category;
- `severity`: operational severity;
- `action`: concise action identifier;
- `target`: affected file/component/service;
- `result`: normalized result;
- `message`: short human-readable sanitized message;
- `next_step`: recommended follow-up if any.

---

## 5.1 Source of truth vs derived logs

Future logging must avoid double primary writes.

Canonical source of truth:

```text
/openclaw/workspace/main/logs/operational_timeline.jsonl
```

Role:

- single structured operational timeline;
- append-only JSONL;
- machine-readable;
- source for dashboards, summaries, alerts and later derived views;
- primary evidence for questions such as `what happened and when?`.

Derived optional human view:

```text
/openclaw/workspace/main/logs/operational_events.log
```

Role:

- readable text projection of the timeline;
- useful for quick manual inspection;
- not the source of truth;
- may be regenerated later from `operational_timeline.jsonl`;
- must not contain information that is absent from the structured timeline.

Future rule:

```text
scripts write primary events to operational_timeline.jsonl only.
operational_events.log, if needed, is derived from the timeline.
```

This avoids:

- duplicate writes;
- mismatched timestamps;
- contradictory event counts;
- divergence between human text logs and structured evidence;
- uncertainty about which log is authoritative.

If a future script cannot write the structured timeline, it should report timeline logging failure and avoid writing only to the derived text log as if it were canonical.

---

## 6. Rules

### 6.1 Append-only

Operational timeline must be append-only.

Allowed:

```text
append one line per event
```

Not allowed:

```text
rewrite history
silently delete events
hide failed events
```

### 6.2 No secrets

Never log:

- tokens;
- `.env` values;
- `openclaw.json` contents;
- API keys;
- private message bodies unless explicitly sanitized and authorized.

### 6.3 No sensitive data

Avoid logging:

- full prompts;
- full user messages;
- full stack traces with paths/secrets;
- raw URLs with query parameters;
- personal data not needed for operations.

### 6.4 Best-effort

Logging must never break the main action.

If logging fails:

```text
main action result remains valid
logging failure is reported separately
no broad repair attempt
```

### 6.5 No action blocking

The logging layer must not:

- restart services;
- call runtime;
- call RAG;
- change gateway;
- modify models;
- access tokens;
- block the original action because logging failed.

---

## 7. Implementation phases

### Fase 1 — diseño

Status:

```text
current phase
```

Actions:

- document logging architecture;
- define schema;
- define rules;
- identify current sources;
- avoid implementation changes.

Validation:

- document readback;
- confirm no scripts/dashboard/runtime/services changed.

### Fase 2 — writer común

Goal:

```text
create one safe writer for operational_timeline.jsonl.
```

Candidate script:

```text
/openclaw/workspace/main/scripts/log_operational_event.py
```

Required behavior:

- accept explicit fields;
- validate allowed severity/result/type values;
- sanitize message;
- append one JSONL line;
- fail best-effort;
- never read secrets;
- never touch runtime/services/RAG.

Validation:

- `python3 -m py_compile`;
- controlled dry event;
- read one appended line;
- confirm valid JSON.

### Fase 3 — conectar `ru_event.sh`

Goal:

```text
MAIN action events also write to operational_timeline.jsonl.
```

Mapping:

```text
flow/action/target/result -> source=MAIN, type=action, severity=info|warning
```

Rules:

- do not duplicate excessive detail;
- preserve existing Resource Usage behavior;
- if timeline write fails, Resource Usage still proceeds.

### Fase 4 — conectar alertas

Goal:

```text
alert scripts append structured alert events.
```

Examples:

```text
restart_detected
brokenpipe_threshold_exceeded
resource_usage_ratio_low
too_many_blocked_actions
```

Rules:

- keep `alerts/alert.txt` as latest human summary;
- structured timeline is the historical source;
- avoid logging false positives from normal HTTP 200 lines.

### Fase 5 — conectar daily summary

Goal:

```text
daily summary send/reset becomes a structured timeline event.
```

Events:

```text
DAILY_SUMMARY_SENT ok
DAILY_SUMMARY_SENT failed
DAILY_SUMMARY_RESET ok
```

Rules:

- reset only after successful send;
- if send fails, keep data for retry;
- log failure without breaking the script.

---

## 8. Recommended query examples

Future queries should be answerable from `operational_timeline.jsonl`:

```text
last 20 events
all warnings today
all failed actions today
last daily summary send status
alerts in the last 2 hours
what happened before a restart alert
```

Possible future helper:

```text
scripts/show_operational_timeline.py
```

This helper should be read-only.

---

## 9. Risk assessment

Design-only risk:

```text
low
```

Future writer risk:

```text
low-medium
```

Runtime integration risk:

```text
high
```

Recommendation:

```text
Do not integrate with runtime. Start with explicit scripts and append-only JSONL writer.
```

---

## 10. Current decision

No implementation yet.

Next safest step, only if explicitly authorized:

```text
Create scripts/log_operational_event.py as a common append-only writer for operational_timeline.jsonl.
```
