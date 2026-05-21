# 22_ASSISTED_EXECUTION_RUNBOOK.md

Status: official MAIN/global runbook  
Scope: ASSISTED_EXECUTION_LOW_SCOPE across `/openclaw/workspace/main`  
Version: v1.1

---

## 1. Purpose

This runbook defines how Neodaemon MAIN applies `ASSISTED_EXECUTION_LOW_SCOPE` in practice.

`ASSISTED_EXECUTION_LOW_SCOPE` is a global safe-execution policy for Neodaemon MAIN. It is not limited to RAG, `rag_ops`, or the Fabric for Welding Data project.

It applies to small, reversible, validated actions inside:

```text
/openclaw/workspace/main
```

including:

- `context_repo`;
- project documentation;
- scripts;
- validation wrappers;
- debugging helpers;
- read-only inspections;
- `git status`, `git diff` and `git log` diagnostics;
- RAG-related work as one use case, not the whole scope.

Core principle:

```text
low scope + explicit path + rollback + validation + no critical blocker + no global prohibition
```

If any required condition fails, Neodaemon must stop and ask Albert for explicit authorization.

---

## 2. MAIN/global scope

This runbook is global for the MAIN workspace.

Allowed scope can include, when explicitly authorized and low-risk:

- Markdown documentation under `/openclaw/workspace/main`;
- `context_repo` project files;
- scripts under `/openclaw/workspace/main/scripts` or `/openclaw/workspace/main/context_repo/scripts`;
- validation-only wrappers;
- read-only debugging scripts;
- local project governance files;
- local dashboards or generated static documentation when explicitly approved;
- read-only Git inspection commands such as `git status`, `git diff`, `git diff --stat` and `git log`.

RAG is only one case:

```text
RAG work follows this runbook, but this runbook is not a RAG-only policy.
```

---

## 3. Fixed execution order

Every assisted low-scope execution must follow this order:

```text
CRITICAL_ENGINE_V2_1 -> TASK_VALIDATOR -> ASSISTED_EXECUTION_LOW_SCOPE -> VALIDATION -> POST_ACTION_REVIEW
```

Meaning:

1. `CRITICAL_ENGINE_V2_1` checks whether the decision is technically sane.
2. `TASK_VALIDATOR` checks operational risk, affected paths, rollback and validation.
3. `ASSISTED_EXECUTION_LOW_SCOPE` executes only one approved low-scope change.
4. `VALIDATION` proves the result as far as available tools allow.
5. `POST_ACTION_REVIEW` decides whether to continue, stop or ask Albert.

Skipping one stage invalidates the action unless Albert explicitly overrides it.

---

## 4. Actions permitted without a new OK

These actions may proceed without a new OK only when Albert has already authorized the current low-scope cycle and every condition in this runbook is satisfied.

Allowed within the current authorized cycle:

- create one Markdown document under an approved path in `/openclaw/workspace/main`;
- update one Markdown document under an approved path;
- add one section to one existing Markdown file;
- create one read-only validation or debugging wrapper under an approved scripts path;
- create one timestamp backup of the single file being modified;
- read back the created or modified file for validation;
- run explicitly authorized read-only validation commands if execution tools are available;
- run read-only Git diagnostics when they are part of the plan;
- report blocked validations honestly.

Allowed read-only Git diagnostics:

```bash
git -C /openclaw/workspace/main status --short
git -C /openclaw/workspace/main diff --stat
git -C /openclaw/workspace/main diff -- <path>
git -C /openclaw/workspace/main log --oneline -n <N>
```

These commands are inspection only. They do not imply permission to commit or push.

---

## 5. Actions requiring human OK

The following always require explicit Albert authorization:

- any write action not already covered by the current TASK_VALIDATOR;
- creating or modifying RAG chunks;
- running `/rag-ask`;
- running wrappers that query a live model or response path;
- modifying `api_rag_v2.py`;
- modifying `rag_loader.py`, `rag_retriever.py` or `rag_filter.py`;
- modifying runtime code;
- restarting services;
- changing prompts;
- changing models;
- changing gateway;
- changing Telegram routing;
- reading or modifying tokens or configuration;
- generating chunks from PDFs;
- ingesting PDFs;
- creating more than one primary file;
- modifying more than one primary file;
- committing;
- pushing;
- running any command not listed in the current TASK_VALIDATOR plan.

If in doubt, ask Albert.

---

## 6. Global prohibitions

The following prohibitions remain active everywhere in `/openclaw/workspace/main`.

ASSISTED_EXECUTION_LOW_SCOPE must never:

- read `.env`;
- read `/openclaw/.env`;
- read `openclaw.json`;
- read `/home/openclaw/.openclaw/openclaw.json`;
- print tokens;
- touch tokens;
- modify gateway;
- modify Telegram routing;
- modify services;
- restart services;
- modify runtime;
- modify `api_rag_v2.py` without explicit separate authorization;
- modify models;
- change model routing;
- install packages;
- use internet;
- use Docker;
- change sandbox;
- run destructive cleanup;
- perform bulk edits;
- perform unapproved writes;
- create multiple chunks;
- perform PDF ingestion;
- generate chunks at scale;
- run `/rag-ask` without explicit authorization;
- commit;
- run `git push` without explicit authorization;
- hide failed validation.

A prohibited action exits low-scope mode immediately.

---

## 7. One low_scope execution per cycle

Default limit:

```text
one low_scope execution per cycle
```

A cycle is one coherent action approved by Albert.

After one low-scope execution, Neodaemon must stop and provide `POST_ACTION_REVIEW` before continuing.

A new cycle requires either:

- explicit Albert authorization; or
- a new TASK_VALIDATOR accepted by Albert.

This prevents quiet scope creep.

---

## 8. Required output format

Every assisted execution report must use this format:

```text
HECHO / HECHO parcial / BLOQUEADO / ERROR

action:
files affected:
backup created:
validation:
blocked validation:
rollback:
unexpected effects:
POST_ACTION_REVIEW:
next recommended step:
```

If shell validation is unavailable, say:

```text
HECHO parcial — VALIDACIÓN BLOQUEADA
```

Never claim full success when mandatory validation could not run.

---

## 9. ERROR_MODE

`ERROR_MODE` activates when anything unexpected happens.

Triggers:

- path mismatch;
- file already exists when creation-only was expected;
- backup fails;
- write fails;
- validation fails;
- shell validation unavailable when it was mandatory;
- unexpected file modified;
- forbidden string detected;
- JSON invalid;
- wrapper returns non-zero;
- Git status shows unexpected changes caused by the action;
- user says stop, blocked or no hacer.

When active:

```text
ERROR_MODE=active
```

Required behavior:

1. Stop immediately.
2. Do not attempt unrelated fixes.
3. Do not create additional files.
4. Do not modify more files.
5. Preserve backup.
6. Report exact error.
7. Recommend rollback or one minimal diagnostic step.
8. Ask Albert before continuing.

---

## 10. Relation with CRITICAL_ENGINE_V2_1

`CRITICAL_ENGINE_V2_1` decides whether the action is technically sane.

Rules:

- If it returns `BLOQUEAR`, do not execute.
- If it returns `CONDICIONADO + piloto`, execute only that pilot scope.
- If it returns `CONDICIONADO`, all listed validations are mandatory.
- If it returns `AUTORIZAR`, continue only if TASK_VALIDATOR also agrees.

`ASSISTED_EXECUTION_LOW_SCOPE` cannot override `CRITICAL_ENGINE_V2_1`.

---

## 11. Relation with TASK_VALIDATOR

`TASK_VALIDATOR` decides whether the action is operationally safe.

It must specify:

- action;
- type;
- risk score;
- affected paths;
- command or operation preview;
- rollback;
- validation;
- safe-to-execute flag.

If TASK_VALIDATOR says human confirmation is required, execution stops until Albert authorizes.

If TASK_VALIDATOR and CRITICAL_ENGINE_V2_1 disagree, use the stricter result.

---

## 12. Validation rules

Every execution must validate the result.

Minimum validation:

- read back created or modified file;
- confirm required sections or required fields;
- confirm only intended path changed when possible;
- report unavailable validation.

Common validation commands when execution tools are available:

```bash
wc -l <file>
grep -n <pattern> <file>
git -C /openclaw/workspace/main status --short
git -C /openclaw/workspace/main diff --stat -- <path>
git -C /openclaw/workspace/main diff -- <path>
git -C /openclaw/workspace/main log --oneline -n 5
python3 -m json.tool <json-file>
bash -n <script>
```

Validation proves form and execution result. It does not prove technical truth.

---

## 13. VALIDACIÓN AUTOMÁTICA CONTROLADA (low_scope)

This flow defines controlled automatic validation for low-scope artifacts.

It is read-only validation only. It does not write, autocorrect, commit, push, touch runtime or call services.

LOW_SCOPE validation is pure structural validation.

It must never depend on repository content, RAG context, external knowledge or semantic inference.

Classification is based only on:

```text
route + type + scope rules
```

Neodaemon must never answer that context is missing for a structurally valid `VALIDAR_LOW_SCOPE` input.

If the route and type are valid, Neodaemon must always return a classification result.

### 13.1 Trigger

Mandatory format:

```text
VALIDAR_LOW_SCOPE <ruta> <tipo>
```

`tipo` is mandatory.

Allowed types:

```text
markdown
json
shell
chunk_pilot
git
```

Paths containing `../` are forbidden.

### 13.2 Automatic low_scope classification

The validation can be classified as `low_scope` only if all conditions are true:

- target path is present;
- type is present and allowed;
- path does not contain `../`;
- path is inside the allowed validation scope;
- file exists, except `type = git` with target `.`;
- action is read-only;
- no write is attempted;
- no runtime, service, gateway, model, token or configuration is touched;
- no `.env` or `openclaw.json` is read;
- `/rag-ask` is not executed;
- no network is used;
- no commit or push is attempted;
- every command belongs to the whitelist.

Wide scopes such as `.` are allowed for `type = git`, but must report a warning:

```text
warnings: scope amplio "."
```

Wide scope is not ERROR_MODE by itself.

If route and type are valid but execution tools are unavailable for `bash -n`, `python3 -m json.tool` or another syntactic validation command, the result must be partial, not an error:

```text
result: partial
structural_validation: ok
syntax_validation: pending
ERROR_MODE: inactive
```

Missing exec capability does not invalidate structural LOW_SCOPE classification.

If any condition fails:

```text
ERROR_MODE=active
RESULT=not_low_scope
```

### 13.3 Allowed commands

Strict whitelist:

```bash
test -e <ruta>
bash -n <script>
python3 -m json.tool <json>
/openclaw/workspace/main/context_repo/scripts/rag_ops/rag_chunk_preflight.sh --pilot <json>
git -C /openclaw/workspace/main/context_repo status --short
git -C /openclaw/workspace/main/context_repo diff --stat -- <path>
git -C /openclaw/workspace/main/context_repo log --oneline -n <N>
```

Full `git diff` is not allowed by default.

It is allowed only if Albert explicitly asks for it:

```bash
git -C /openclaw/workspace/main/context_repo diff -- <path>
```

### 13.4 Prohibited commands and patterns

Forbidden:

```text
curl
systemctl
journalctl
rm
cp
mv
sed -i
python scripts that write
/rag-ask
git add
git commit
git push
full git diff unless explicitly requested
paths containing ../
```

### 13.5 Execution order by type

Common step 0:

```text
0. confirm path does not contain ../
1. confirm file exists with test -e <ruta>
```

Exception:

```text
type = git and ruta = .
```

`markdown`:

```text
0. check path has no ../
1. check file exists
2. git -C /openclaw/workspace/main/context_repo diff --stat -- <path>
3. git -C /openclaw/workspace/main/context_repo status --short
4. noise control: warning if git status shows changes outside target
5. POST_ACTION_REVIEW
```

`json`:

```text
0. check path has no ../
1. check file exists
2. python3 -m json.tool <json>
3. git -C /openclaw/workspace/main/context_repo diff --stat -- <path>
4. git -C /openclaw/workspace/main/context_repo status --short
5. noise control: warning if git status shows changes outside target
6. POST_ACTION_REVIEW
```

`chunk_pilot`:

```text
0. check path has no ../
1. check file exists
2. python3 -m json.tool <json>
3. /openclaw/workspace/main/context_repo/scripts/rag_ops/rag_chunk_preflight.sh --pilot <json>
4. git -C /openclaw/workspace/main/context_repo diff --stat -- <path>
5. git -C /openclaw/workspace/main/context_repo status --short
6. noise control: warning if git status shows changes outside target
7. POST_ACTION_REVIEW
```

`shell`:

```text
0. check path has no ../
1. check file exists
2. bash -n <script>
3. git -C /openclaw/workspace/main/context_repo diff --stat -- <path>
4. git -C /openclaw/workspace/main/context_repo status --short
5. noise control: warning if git status shows changes outside target
6. POST_ACTION_REVIEW
```

`git`:

```text
0. check path has no ../
1. if ruta = ., no specific file is required
2. git -C /openclaw/workspace/main/context_repo status --short
3. git -C /openclaw/workspace/main/context_repo diff --stat
4. POST_ACTION_REVIEW
```

### 13.6 Git status noise control

After:

```bash
git -C /openclaw/workspace/main/context_repo status --short
```

compare output with the target path.

If there are changes outside the target:

```text
WARNING=changes_outside_target
```

Report the warning, but do not autocorrect.

If outside changes are unexpected or numerous:

```text
ERROR_MODE=active
```

and ask Albert for instruction.

### 13.7 Mandatory output format

```text
VALIDACIÓN AUTOMÁTICA CONTROLADA

trigger:
target:
type:
classification: low_scope | rejected
commands_run:
result:
errors:
warnings:
git_status_noise:
files_changed:
validation_summary:
POST_ACTION_REVIEW:
next_step:
```

### 13.8 ERROR_MODE for controlled validation

Activate if:

- type is missing;
- type is not allowed;
- path contains `../`;
- path is out of allowed scope;
- file does not exist;
- command is not allowed;
- command fails;
- a write attempt appears;
- `.env` is detected;
- `openclaw.json` is detected;
- `/rag-ask` is attempted;
- full `git diff` is attempted without explicit request;
- `git status` shows unexpected changes outside target;
- wrapper is missing;
- JSON validation fails;
- preflight fails;
- `bash -n` fails.

Do not activate ERROR_MODE because repository content is unknown or because contextual knowledge is missing.

`VALIDAR_LOW_SCOPE` must not escalate to contextual reasoning, RAG, or content inference.

Required output:

```text
ERROR_MODE=active
failure:
target:
command_failed:
rollback_required: no
autocorrection: forbidden
next_step:
```

Rules:

```text
No autocorrection.
No file creation.
No file modification.
No retry with unauthorized alternative commands.
```

### 13.9 Final rule

This flow validates only.

```text
read-only validation only
no autocorrection
no writes
no commit
no push
no runtime
no services
no full git diff unless Albert explicitly asks
no ../ paths
```

### 13.10 Resource usage logging status

Estimated resource usage logging exists, but it is not automatically integrated into `VALIDAR_LOW_SCOPE` or `ASSISTED_EXECUTION`.

Writer:

```text
/openclaw/workspace/main/scripts/log_resource_usage.py
```

Log path:

```text
/openclaw/workspace/main/logs/resource_usage.jsonl
```

Current state:

```text
manual logging only
```

Current usage:

```bash
python3 scripts/log_resource_usage.py \
  --flow VALIDAR_LOW_SCOPE \
  --action <short_action> \
  --target <path_or_action> \
  --input-chars <n> \
  --output-chars <n> \
  --result ok
```

Rule:

- events may be registered manually for later analysis;
- manual logging must not imply automatic runtime integration;
- missing resource usage event is not an execution failure while logging remains manual.

Limitation:

```text
No automatic integration exists in VALIDAR_LOW_SCOPE or ASSISTED_EXECUTION.
```

Future note:

```text
Automatic integration requires runtime modification and separate explicit authorization.
```

---

## 14. Rollback rules

Rollback must be known before execution.

For a new file:

```bash
rm <file>
```

For an existing file:

```bash
cp <file>.bak-<timestamp> <file>
```

For a single new script:

```bash
rm <script-file>
```

For a single new local project artifact:

```bash
rm <artifact-file>
```

Rollback must never require service restart unless Albert separately authorizes it.

---

## 15. Concrete allowed examples

### Example A — create one MAIN documentation file

Allowed if path is explicit and validation is defined.

```text
create one Markdown document under /openclaw/workspace/main/context_repo/projects/<project>/
```

Validation:

- read back file;
- `wc -l` if available;
- `git diff --stat` if available;
- `git status --short` if available.

### Example B — add one section to an existing Markdown file

Allowed with backup.

```text
add one section to one existing rule document
```

Validation:

- grep required section;
- confirm forbidden strings absent;
- diff stat.

### Example C — create one read-only debugging wrapper

Allowed if wrapper does not write, does not call external systems and does not touch prohibited paths.

Validation:

- read wrapper;
- `bash -n` if available;
- run only if explicitly authorized.

### Example D — run Git inspection

Allowed when included in the plan.

```bash
git -C /openclaw/workspace/main status --short
git -C /openclaw/workspace/main diff --stat
```

Not allowed:

```bash
git commit
git push
```

### Example E — RAG as a case of use

RAG work can use this runbook for low-scope steps such as one pilot chunk or one read-only wrapper, but RAG remains subject to stricter RAG-specific rules.

RAG-specific actions such as `/rag-ask`, chunk creation, prompt changes or runtime changes require explicit authorization.

---

## 16. Concrete blocked examples

### Blocked A — create several files

Blocked because it violates one-change-per-execution and increases review risk.

### Blocked B — modify documentation and runtime together

Blocked because it mixes low-scope docs with system behavior.

### Blocked C — run `/rag-ask` after creating a chunk without separate authorization

Blocked because live response generation is a separate validation step.

### Blocked D — fix a wrapper and then rerun all tests without a new check

Blocked because it adds unplanned changes after an error.

### Blocked E — commit or git push after validation passes

Blocked because commit and `git push` always require explicit authorization.

### Blocked F — inspect tokens or configuration to unblock validation

Blocked because tokens, `.env`, `openclaw.json`, gateway and runtime configuration are outside low-scope execution.

---

## 17. Final rule

`ASSISTED_EXECUTION_LOW_SCOPE` is permission to execute one small safe MAIN step, not permission to keep going.

After each execution:

```text
stop -> review -> ask or wait
```

If the next action is not already covered by the current authorization, ask Albert.
