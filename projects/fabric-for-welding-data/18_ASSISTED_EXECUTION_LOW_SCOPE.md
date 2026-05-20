# ASSISTED_EXECUTION_LOW_SCOPE

Status: official operational policy  
Scope: small, reversible and validated actions inside the Fabric for Welding Data project  
Version: v1.0

---

## 1. Purpose

ASSISTED_EXECUTION_LOW_SCOPE defines how Neodaemon may execute small and medium-small tasks with assisted automation while preserving Albert's control.

This mode is not autonomous execution.

It exists to allow safe progress when an action is:

- low scope;
- reversible;
- validated;
- constrained to approved paths;
- already reviewed by CRITICAL_ENGINE_V2_1 and TASK_VALIDATOR.

The purpose is to reduce friction for routine safe work without allowing uncontrolled changes.

---

## 2. Core rule

Neodaemon does not decide for Albert.

Neodaemon may execute only when the action satisfies all mandatory conditions in this policy.

If any condition fails, execution must stop and return to explicit human authorization.

---

## 3. What can be automated

The following actions may be executed under ASSISTED_EXECUTION_LOW_SCOPE when authorized by policy and validation is possible:

- create one Markdown document inside an approved project folder;
- update one Markdown document inside an approved project folder;
- create one JSON chunk pilot inside an approved RAG chunk folder;
- create one backup timestamp before modifying a single file;
- validate file existence by reading it back;
- validate JSON structure when an execution tool is available;
- run approved read-only wrappers;
- run approved syntax checks such as `bash -n` or `python3 -m py_compile` when explicitly allowed;
- run read-only `wc`, `grep`, `git diff --stat` or `git status --short` when explicitly allowed;
- produce a concise execution report.

---

## 4. What can never be automated in this mode

ASSISTED_EXECUTION_LOW_SCOPE must never perform:

- service restart;
- gateway modification;
- Telegram routing changes;
- token access;
- `.env` access;
- `openclaw.json` access;
- model changes;
- sandbox changes;
- Docker changes;
- package installation;
- internet access;
- `/rag-ask` execution unless separately authorized;
- PDF ingestion;
- massive chunk generation;
- bulk file edits;
- commit;
- push;
- destructive deletion outside a clearly authorized rollback;
- changes to `api_rag_v2.py`;
- changes to `rag_loader.py`, `rag_retriever.py` or `rag_filter.py`;
- active automation creation or enabling;
- any action with unclear rollback.

If a task requires any of these, it exits ASSISTED_EXECUTION_LOW_SCOPE and returns to explicit human authorization.

---

## 5. Mandatory conditions

All conditions must be true before execution:

1. The action is low scope.
2. The action affects one primary file only.
3. The path is explicit and approved.
4. The action is reversible.
5. Rollback is defined before execution.
6. Validation is defined before execution.
7. CRITICAL_ENGINE_V2_1 has not returned `BLOQUEAR`.
8. TASK_VALIDATOR has classified the action as safe or conditionally safe.
9. The action does not touch runtime RAG code.
10. The action does not touch services.
11. The action does not touch tokens or configuration.
12. The output format is known.
13. The final report can prove what changed.

If any condition is false or unknown:

```text
STOP -> return to Albert for explicit authorization
```

---

## 6. Whitelist

Allowed low-scope targets, when explicitly requested or already authorized:

- project Markdown files under:
  `/openclaw/workspace/main/context_repo/projects/fabric-for-welding-data/`
- project rule files under:
  `/openclaw/workspace/main/context_repo/projects/fabric-for-welding-data/rag_rules/`
- a single pilot JSON chunk under:
  `/openclaw/workspace/main/rag_store/chunks_v2/`
- approved read-only wrapper scripts under:
  `/openclaw/workspace/main/context_repo/scripts/rag_ops/`

Allowed validation commands, when execution tools are available and the command is explicitly part of the plan:

- `wc -l <approved-file>`
- `grep -n <approved-pattern> <approved-file>`
- `git -C /openclaw/workspace/main diff --stat -- <approved-path>`
- `git -C /openclaw/workspace/main status --short`
- `python3 -m json.tool <approved-json>`
- `bash -n <approved-wrapper>`

---

## 7. Blacklist

Never use this mode for:

- `/openclaw/api_rag_v2.py`
- `/openclaw/rag_loader.py`
- `/openclaw/rag_retriever.py`
- `/openclaw/rag_filter.py`
- `/openclaw/.env`
- `/home/openclaw/.openclaw/openclaw.json`
- gateway configuration;
- Telegram bot routing;
- systemd service modification or restart;
- tokens and secrets;
- external network access;
- Git commit or push;
- mass generation of chunks;
- PDF ingestion;
- destructive cleanup;
- multi-file refactors.

---

## 8. One-change-per-execution rule

Each assisted execution may contain only one primary change.

Allowed examples:

- create one Markdown file;
- update one Markdown file;
- create one pilot JSON chunk;
- create one wrapper script;
- add one section to one document.

Not allowed:

- create multiple chunks;
- update rules and chunks in the same execution;
- modify documentation and runtime code together;
- run validation plus unrelated cleanup;
- create files and commit them in the same execution.

If the task naturally requires multiple changes, split it into separate executions.

---

## 9. Mandatory validation

Every assisted execution must include validation.

Minimum validation:

- read back the changed file;
- confirm required sections or required fields;
- report whether shell validation was possible;
- report blocked validations honestly.

When execution tools are available, use the validation defined in the task, such as:

- `wc -l`;
- `grep`;
- `git diff --stat`;
- `git status --short`;
- `python3 -m json.tool`;
- approved read-only wrapper output.

If validation cannot be performed, final status must say:

```text
HECHO parcial / VALIDACIÓN BLOQUEADA
```

Do not claim full validation when only read-back validation was possible.

---

## 10. Mandatory rollback

Rollback must be defined before execution.

For a new file:

```text
rollback = remove the created file
```

For an existing file:

```text
rollback = restore timestamp backup
```

For a JSON chunk:

```text
rollback = remove new chunk or restore previous backup
```

Rollback must not rely on service restart unless separately authorized.

If rollback is unclear, execution is not allowed.

---

## 11. Relation with CRITICAL_ENGINE_V2_1

CRITICAL_ENGINE_V2_1 runs before ASSISTED_EXECUTION_LOW_SCOPE.

It decides whether the action is technically sane.

Rules:

- If CRITICAL_ENGINE_V2_1 returns `BLOQUEAR`, assisted execution cannot proceed.
- If it returns `CONDICIONADO + piloto`, assisted execution may proceed only inside the proposed pilot scope.
- If it returns `CONDICIONADO`, all required validations must be satisfied.
- If it returns `AUTORIZAR`, execution can proceed if TASK_VALIDATOR also permits it.

ASSISTED_EXECUTION_LOW_SCOPE cannot override CRITICAL_ENGINE_V2_1.

---

## 12. Relation with TASK_VALIDATOR

TASK_VALIDATOR runs before execution and checks operational risk.

It must provide:

- action;
- type;
- risk score;
- affected paths;
- command or operation preview;
- rollback;
- validation;
- safe-to-execute flag.

ASSISTED_EXECUTION_LOW_SCOPE may execute only when TASK_VALIDATOR allows the action under the current authorization rules.

If TASK_VALIDATOR requires human confirmation, execution stops until Albert confirms.

---

## 13. Examples allowed

Allowed example 1:

```text
Create one Markdown policy file in context_repo/projects/fabric-for-welding-data/.
```

Why allowed:

- one file;
- documentation only;
- reversible;
- validation possible.

Allowed example 2:

```text
Add one section to WELDING_CHUNK_VALIDATION_RULES.md.
```

Why allowed:

- one file;
- no runtime impact;
- backup possible;
- grep validation possible.

Allowed example 3:

```text
Create one pilot JSON chunk with text + content, validation = B, status = review.
```

Why allowed:

- one pilot;
- reversible;
- JSON validation possible;
- BM25 validation possible;
- no runtime file touched.

Allowed example 4:

```text
Create one read-only wrapper script under context_repo/scripts/rag_ops/.
```

Why allowed:

- one file;
- wrapper is read-only;
- syntax validation possible;
- no service restart.

---

## 14. Examples blocked

Blocked example 1:

```text
Create 10 chunks at once.
```

Reason:

- not low scope;
- contamination risk;
- BM25 validation not isolated.

Blocked example 2:

```text
Modify api_rag_v2.py and restart the RAG service.
```

Reason:

- runtime code;
- service action;
- high impact.

Blocked example 3:

```text
Read .env to confirm token configuration.
```

Reason:

- token/secret risk.

Blocked example 4:

```text
Run /rag-ask after creating a chunk.
```

Reason:

- requires separate authorization.

Blocked example 5:

```text
Ingest a PDF and generate chunks automatically.
```

Reason:

- bulk generation;
- high contamination risk;
- requires separate pipeline validation.

---

## 15. Failure handling

If execution fails:

1. Stop immediately.
2. Do not attempt unrelated fixes.
3. Report what succeeded and what failed.
4. Preserve backup if created.
5. Recommend rollback or next diagnostic step.
6. Return to Albert for confirmation if the next step is outside low scope.

If validation fails:

1. Do not continue.
2. Do not commit or push.
3. Mark result as `ERROR` or `BLOQUEADO`.
4. Recommend rollback or minimal correction.

---

## 16. Final rule

ASSISTED_EXECUTION_LOW_SCOPE is assisted execution, not autonomy.

It allows Neodaemon to execute small safe steps only when:

```text
low scope + reversible + validated + authorized by policy + no critical blocker
```

If any part is missing:

```text
return to explicit human authorization
```
