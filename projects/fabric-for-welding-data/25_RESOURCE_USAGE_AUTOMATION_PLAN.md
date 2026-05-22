# 25_RESOURCE_USAGE_AUTOMATION_PLAN.md

Status: analysis only  
Scope: safe path from manual to semi-automatic resource usage logging  
Version: v1.0

---

## 1. Purpose

Define a safe plan to move `resource_usage` from manual logging to semi-automatic or automatic logging for MAIN flows.

Target flows:

- `VALIDAR_LOW_SCOPE`
- `ASSISTED_EXECUTION`

This document is analysis only.

No code is implemented here.

---

## 2. Current state

Current state:

```text
logging manual
```

Existing writer:

```text
/openclaw/workspace/main/scripts/log_resource_usage.py
```

Existing log path:

```text
/openclaw/workspace/main/logs/resource_usage.jsonl
```

Existing static dashboard export path:

```text
/openclaw/workspace/main/dashboard-v2/data/resource_usage.json
```

Current limitation:

- events are not generated automatically by `VALIDAR_LOW_SCOPE`;
- events are not generated automatically by `ASSISTED_EXECUTION`;
- missing events do not mean the action failed;
- logging depends on explicit manual call or manually written event.

---

## 3. What is missing for automatic events

To register events automatically, the system needs one of these control points:

1. a wrapper that users/MAIN call instead of raw validation commands;
2. a MAIN-side protocol hook that calls the writer after each relevant action;
3. a runtime integration point inside OpenClaw execution/message handling.

Minimum required inputs per event:

```text
timestamp
flow
action
target
input_chars
output_chars
total_chars
estimated_tokens
result
usage_limit
```

Missing today:

- reliable automatic capture of input/output character counts;
- a central place where all `VALIDAR_LOW_SCOPE` results pass as code;
- a central place where all `ASSISTED_EXECUTION` results pass as code;
- deduplication rules;
- error handling policy if logging fails;
- guarantee that logging failures never block the main task.

---

## 4. Options

## Option 1 — manual controlled logging

Description:

```text
Keep current writer and call it manually when useful.
```

Files touched:

- no additional files required;
- optionally update documentation only.

Pros:

- lowest risk;
- no runtime changes;
- no service restart;
- no hidden automation;
- easy rollback.

Cons:

- incomplete data;
- depends on operator discipline;
- cannot reliably compare all flows;
- easy to forget.

Risks:

- underreporting;
- inconsistent `input_chars` / `output_chars` estimates;
- manual events may not match exact action boundaries.

Validation needed:

- read `logs/resource_usage.jsonl`;
- confirm JSONL validity when exec is available;
- confirm dashboard export still works when run manually.

Risk level:

```text
low
```

---

## Option 2 — wrapper externo

Description:

```text
Create a dedicated wrapper for controlled validation/execution that calls log_resource_usage.py after completing the action.
```

Example concept:

```text
scripts/validar_low_scope.py
scripts/assisted_execution_log_wrapper.py
```

The wrapper would:

1. receive flow/action/target/result;
2. run only allowed read-only validation commands;
3. estimate input/output characters;
4. call or import the existing writer;
5. append one JSONL event;
6. never modify target files.

Files likely touched:

- new wrapper script under `/openclaw/workspace/main/scripts/`;
- possibly `22_ASSISTED_EXECUTION_RUNBOOK.md` documentation;
- `logs/resource_usage.jsonl` during validation.

Pros:

- no OpenClaw runtime changes;
- no endpoint changes;
- no service restart;
- can be piloted with `VALIDAR_LOW_SCOPE` first;
- easier to validate and rollback;
- keeps automation explicit.

Cons:

- only works when the wrapper is used;
- does not capture conversational actions automatically;
- wrapper design must avoid writing except to the log;
- still requires exec availability.

Risks:

- accidental expansion into command runner;
- duplicate events if MAIN also logs manually;
- incorrect result classification if wrapper is too generic;
- hidden write risk if validation commands are not strictly whitelisted.

Controls:

- strict command whitelist;
- append-only JSONL write only;
- no target writes;
- no `/rag-ask`;
- no runtime/service/gateway/model/token access;
- deduplication by not allowing manual log for same wrapper event.

Validation needed:

- `bash -n` or `python3 -m py_compile` for wrapper;
- run one controlled `VALIDAR_LOW_SCOPE` dry case;
- confirm exactly one new JSONL line;
- validate JSONL line fields;
- confirm no target file changed;
- confirm dashboard export reads the new event.

Risk level:

```text
low-medium
```

---

## Option 3 — integración runtime

Description:

```text
Modify OpenClaw/runtime or MAIN execution pipeline so events are emitted automatically after relevant actions.
```

Files likely touched:

- OpenClaw runtime code or agent execution handler;
- possibly gateway/runtime configuration;
- logging module;
- tests or validation scripts.

Pros:

- most complete data;
- can capture all relevant actions consistently;
- less dependent on manual discipline;
- better long-term observability.

Cons:

- highest operational risk;
- may require service restart;
- touches runtime behavior;
- risk of logging sensitive content if boundaries are wrong;
- harder rollback;
- requires stronger testing.

Risks:

- runtime instability;
- duplicated or excessive logging;
- logging secrets or private content;
- performance overhead;
- breaking MAIN action flow;
- creating misleading usage data if estimates are wrong;
- interaction with gateway/services.

Validation needed:

- code review;
- unit/smoke test;
- syntax/type validation;
- dry-run event generation;
- service-level validation if runtime is touched;
- verify no secrets are logged;
- rollback plan before deployment.

Risk level:

```text
high
```

---

## 5. Recommendation

Recommended lowest-risk path:

```text
Option 2 — wrapper externo, piloted only for VALIDAR_LOW_SCOPE
```

Reason:

- avoids runtime changes;
- avoids dashboard changes;
- avoids services;
- keeps behavior explicit and reversible;
- can generate real events automatically when the wrapper is used;
- can be validated with one controlled event.

Do not start with runtime integration.

Runtime integration should only be considered after the wrapper proves useful and safe.

---

## 6. Minimal phased plan

### Phase 0 — current state

Keep manual logging.

No change.

### Phase 1 — define wrapper contract

Create a document or update runbook with:

- allowed inputs;
- allowed flows;
- allowed commands;
- result mapping;
- deduplication rule;
- logging failure rule.

No code yet.

### Phase 2 — pilot wrapper for VALIDAR_LOW_SCOPE

Create one wrapper script only if explicitly authorized.

Scope:

- read-only validation;
- log exactly one event per invocation;
- no target writes;
- no runtime;
- no RAG;
- no services.

### Phase 3 — validate end-to-end manually

Run one controlled validation:

```text
VALIDAR_LOW_SCOPE . git
```

Expected:

- validation result produced;
- exactly one new JSONL line;
- `usage_limit = false` by default;
- dashboard export can include the event.

### Phase 4 — consider ASSISTED_EXECUTION wrapper

Only after Phase 2 is stable.

Scope must remain narrow:

- log action summaries;
- avoid logging sensitive content;
- never block the original action because logging failed.

### Phase 5 — consider runtime integration

Only with separate explicit authorization.

Requires stronger review and rollback.

---

## 7. Files that may need changes later

For wrapper approach:

```text
/openclaw/workspace/main/scripts/validar_low_scope.py
/openclaw/workspace/main/scripts/log_resource_usage.py
/openclaw/workspace/main/context_repo/projects/fabric-for-welding-data/22_ASSISTED_EXECUTION_RUNBOOK.md
/openclaw/workspace/main/logs/resource_usage.jsonl
```

For dashboard export after events exist:

```text
/openclaw/workspace/main/scripts/export_resource_usage_dashboard.py
/openclaw/workspace/main/dashboard-v2/data/resource_usage.json
```

For runtime integration only if later authorized:

```text
OpenClaw runtime / MAIN execution handler file, exact path pending discovery
```

Files not required for the recommended pilot:

```text
gateway config
service units
RAG runtime
dashboard-v2/index.html
dashboard-v2/tools/resource-usage.html
```

---

## 8. Required validations

Minimum validations for wrapper pilot:

- read script;
- syntax validation: `python3 -m py_compile <wrapper>` when exec is available;
- run one controlled low-scope validation;
- read `logs/resource_usage.jsonl`;
- confirm exactly one new event;
- confirm required fields exist;
- confirm `estimated_tokens = total_chars / 4` approximately;
- confirm `usage_limit = false` by default;
- confirm no target file changed;
- confirm no commit/push.

If exec is unavailable:

```text
syntax_validation: pending
execution_validation: pending
```

---

## 9. Logging failure rule

Logging must never break the original safe action.

If validation succeeds but logging fails:

```text
result: partial
validation_result: ok
resource_usage_logging: failed
ERROR_MODE: inactive unless the logging failure indicates broader filesystem/runtime damage
```

The failure must be reported, but the wrapper must not attempt broad repairs.

---

## 10. Final decision

Do not touch runtime yet.

Next safest executable step, if Albert authorizes later:

```text
Create a read-only VALIDAR_LOW_SCOPE wrapper that logs exactly one resource_usage event per invocation.
```

---

## 11. Operational counting rule

Status: active operational protocol for MAIN, without runtime integration.

From now on, every relevant MAIN action must register one Resource Usage event using the manual wrapper:

```bash
bash /openclaw/workspace/main/scripts/ru_event.sh \
  <flow> \
  <action> \
  <target> \
  <result>
```

This rule does not automate runtime behavior. It is a MAIN-side operating discipline.

Events must be added when an action ends with any of these outcomes or categories:

- `HECHO`;
- `HECHO parcial`;
- `BLOQUEADO`;
- `ERROR_MODE`;
- validation OK;
- dashboard change;
- file creation or modification;
- service activation or verification;
- relevant manual execution.

Result mapping:

```text
HECHO          -> ok
HECHO parcial  -> partial
BLOQUEADO      -> blocked
real error     -> error
```

Allowed flows:

```text
EPCODM
VALIDAR_LOW_SCOPE
ASSISTED_EXECUTION
DASHBOARD
LTU
SYSTEMD
GIT
RAG_PAUSED
TEST
OTHER
```

Operational constraints:

- do not touch OpenClaw runtime;
- do not touch services;
- do not touch RAG runtime;
- do not modify scripts as part of this rule;
- do not create internal automation yet;
- do not commit/push unless explicitly authorized.

Expected behavior of `ru_event.sh`:

1. append one event to `/openclaw/workspace/main/logs/resource_usage.jsonl` through `log_resource_usage.py`;
2. refresh `/openclaw/workspace/main/dashboard-v2/data/resource_usage.json` through `update_resource_usage_dashboard.sh`;
3. use default estimates unless a more specific wrapper is later authorized.

If Resource Usage logging fails after the main action succeeded, the main action is reported as done and the Resource Usage registration is reported separately as `partial` or `error`. Logging failure must not trigger runtime repairs or broad service changes.

---

## 12. Level 2 – Relevant Action Definition

Status: active criterion for Resource Usage Level 2.

Goal:

```text
Avoid noise and register only events with real operational value.
```

At Level 2, a Resource Usage event must be registered only when at least one of these conditions is true:

- there is a change in system state, files, or configuration;
- there is real execution of an action;
- there is an explicit operational decision or terminal outcome, such as:
  - `HECHO`;
  - `BLOQUEADO`;
  - `ERROR`;
  - validation completed.

Events must not be registered for:

- chat text by itself;
- explanations;
- plans or proposals without execution;
- diagnosis without action;
- intermediate reasoning;
- discussion that does not end in a concrete action, change, validation, block, or error.

Practical rule:

```text
If nothing changed, nothing ran, and no explicit result was decided, do not log a Resource Usage event.
```

Examples that should be logged:

- a Markdown file is created or updated;
- a validation command is actually executed;
- a task is explicitly marked `HECHO` after verification;
- a task is explicitly marked `BLOQUEADO` because authorization or safe prerequisites are missing;
- an action ends in `ERROR` or partial failure.

Examples that should not be logged:

- Albert sends instructions;
- MAIN explains a plan but does not execute it;
- MAIN gives a diagnostic opinion without running validation or changing files;
- a conversation clarifies scope but produces no action or decision.

Level 2 therefore counts relevant operational events, not conversational turns.

---

## 13. TEST flow convention

Status: active convention for future Resource Usage events.

Use flow:

```text
TEST
```

for technical tests, pipeline validations and artificial events.

Examples:

- Resource Usage exporter test;
- metrics pipeline test;
- dashboard refresh test;
- synthetic event used to verify logging behavior.

Do not use `EPCODM` for infrastructure tests.

`EPCODM` must remain reserved for actual EPCODM-governed operational changes or decisions.

Historical rule:

```text
Do not rewrite already registered historical events only to change their flow.
```

If older test events were logged under `EPCODM`, keep them as historical record and use `TEST` from this point forward.
