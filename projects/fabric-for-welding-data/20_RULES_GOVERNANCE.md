# 20_RULES_GOVERNANCE.md

Status: official governance policy  
Scope: rule governance for Fabric for Welding Data, RAG rules, RD interpretation and assisted execution  
Version: v1.0

---

## 1. Purpose

This document defines rule governance for the Fabric for Welding Data project.

Its purpose is to prevent:

- rule drift;
- duplicated policies;
- uncontrolled overengineering;
- contradictory instructions;
- documentation chaos;
- unsafe expansion of RAG knowledge;
- confusing technical validation with technical truth.

Rules must help execution, not create paralysis.

---

## 2. Fixed decision order

Every relevant action must follow this fixed order:

```text
CRITICAL_ENGINE_V2_1 -> TASK_VALIDATOR -> ASSISTED_EXECUTION -> VALIDACIÓN -> POST_ACTION_REVIEW
```

Meaning:

1. `CRITICAL_ENGINE_V2_1` checks whether the decision is technically sane.
2. `TASK_VALIDATOR` checks operational risk, affected paths, rollback and validation.
3. `ASSISTED_EXECUTION` executes only if scope, reversibility and validation allow it.
4. `VALIDACIÓN` confirms the result with the smallest meaningful checks.
5. `POST_ACTION_REVIEW` records whether the action actually improved the system.

Skipping one stage invalidates the action unless Albert explicitly overrides it.

---

## 3. task_type

Every governed action must declare one `task_type`.

Allowed values:

```text
docs
rag
system
analysis
```

### docs

Documentation-only change.

Examples:

- create policy Markdown;
- update rule document;
- add governance section.

Default risk: low, unless it changes operational rules that affect RAG behavior.

### rag

RAG knowledge, retrieval, prompts, chunks or RAG quality.

Examples:

- create pilot chunk;
- modify chunk rules;
- validate BM25 behavior;
- change RAG prompt.

Default risk: medium, because it can affect answers.

### system

Runtime, services, gateway, Telegram, tokens, configuration or code paths.

Examples:

- modify `api_rag_v2.py`;
- restart services;
- change loader/retriever/filter;
- edit gateway configuration.

Default risk: high.

### analysis

Read-only reasoning or investigation.

Examples:

- inspect docs;
- reconstruct state;
- compare risks;
- run CRITICAL_ENGINE without writing.

Default risk: low, unless it requests sensitive files.

---

## 4. Rule drift control

Rule drift happens when new rules silently contradict, duplicate or weaken existing rules.

Before adding or changing a rule, check:

- Does an existing rule already cover this?
- Does the new rule contradict CRITICAL_ENGINE_V2_1?
- Does the new rule contradict ASSISTED_EXECUTION_LOW_SCOPE?
- Does it use valid `validation/status` values?
- Does it claim the loader filters fields it does not actually filter?
- Does it make provisional criteria look final?
- Does it create more process than the task needs?

If the new rule duplicates an existing rule, prefer updating the existing rule instead of adding another document.

If the new rule is narrower, place it in the closest existing document.

If the new rule defines a new operating mode, create a new numbered document.

---

## 5. Deprecated rules

A rule becomes `deprecated` when:

- it uses an invalid status value, such as `conditioned`;
- it contradicts the confirmed loader contract;
- it assumes fields are active filters when they are only metadata;
- it encourages RD as final quality diagnosis;
- it treats provisional thresholds as fixed truth;
- it requires unavailable validation;
- it duplicates a newer rule with less precision;
- it increases process without improving safety or quality.

Deprecated rules must not be used for new actions.

If a deprecated rule remains in a document for historical context, it must be clearly marked:

```text
DEPRECATED: do not use for new decisions.
```

Preferred action is to replace deprecated rules with corrected wording during the next low-scope documentation update.

---

## 6. Low_scope execution limit per cycle

Low-scope assisted execution is allowed to avoid friction, but it must not become uncontrolled autonomy.

Default limit:

```text
maximum 3 low_scope executions per cycle
```

A cycle means one coherent work session around a single goal.

After 3 low_scope executions, Neodaemon must pause and perform POST_ACTION_REVIEW before continuing.

The review must answer:

- What changed?
- Did validation pass?
- Did scope creep occur?
- Are we still aligned with the original goal?
- Should we continue, stop or ask Albert?

Albert can explicitly authorize a new cycle.

---

## 7. ERROR_MODE

ERROR_MODE is activated when an execution, validation or assumption fails.

Triggers:

- validation command fails;
- expected file is missing;
- unexpected file changed;
- JSON invalid;
- BM25 does not retrieve the expected chunk;
- forbidden string appears, such as `status = conditioned`;
- runtime file is touched unintentionally;
- rollback path is unclear;
- tool access is blocked;
- result cannot be verified.

When ERROR_MODE is active:

1. Stop immediately.
2. Do not continue with adjacent fixes.
3. Do not create additional files.
4. Do not commit or push.
5. Report exact failure.
6. Preserve backups.
7. Recommend rollback or one minimal diagnostic step.
8. Return to Albert if the next step is not low scope.

ERROR_MODE output must include:

```text
ERROR_MODE=active
failure=<specific failure>
affected_path=<path>
rollback=<available rollback>
next_step=<minimal next step>
```

---

## 8. Confidence levels

Every significant recommendation should include confidence.

Allowed values:

```text
confidence: low | medium | high
```

### low

Use when:

- source is incomplete;
- loader/runtime behavior is not confirmed;
- data semantics are unknown;
- validation is blocked;
- conclusion is mostly inferred.

Action: do not execute beyond read-only or documentation unless Albert authorizes.

### medium

Use when:

- source is partially confirmed;
- rollback exists;
- validation is possible;
- impact is low or medium;
- uncertainty is tolerable.

Action: allow conditioned pilot or low-scope documentation.

### high

Use when:

- source is confirmed;
- contract is known;
- validation is available;
- rollback exists;
- impact is low;
- no critical contradictions exist.

Action: allow execution under ASSISTED_EXECUTION_LOW_SCOPE if TASK_VALIDATOR agrees.

---

## 9. POST_ACTION_REVIEW

POST_ACTION_REVIEW is mandatory after every write action.

Minimum review:

```text
POST_ACTION_REVIEW
- action completed:
- files changed:
- validation result:
- blocked validations:
- rollback available:
- unexpected effects:
- confidence:
- next recommended step:
```

For RAG-related actions, also include:

- retrieval impact expected;
- BM25 validation status;
- whether the chunk/rule may contaminate answers;
- whether the action should remain pilot, review or approved.

If validation is blocked, the review must say so explicitly.

Do not report full success when validation was only partial.

---

## 10. Technical validation is not technical truth

Passing validation means the artifact is syntactically or operationally acceptable.

It does not mean the technical claim is true.

Examples:

- JSON valid does not mean the welding rule is correct.
- BM25 retrieval does not mean the answer is technically safe.
- `py_compile` passing does not mean runtime behavior is good.
- A chunk appearing in top results does not mean it should drive decisions.
- A rule being documented does not mean it is scientifically validated.

For RD and welding:

```text
validation confirms form and retrieval; real production data confirms technical truth.
```

Therefore, any rule involving RD, nugget, quality, stability or thresholds must clearly separate:

- confirmed technical fact;
- provisional criterion;
- monitoring signal;
- hypothesis;
- forbidden inference.

---

## 11. Rule duplication control

Before adding a new governance document, check whether the content belongs in:

- `17_CRITICAL_ENGINE_V2_1.md`;
- `18_ASSISTED_EXECUTION_LOW_SCOPE.md`;
- `WELDING_CHUNK_VALIDATION_RULES.md`;
- this document.

Guideline:

- decision quality -> `17_CRITICAL_ENGINE_V2_1.md`;
- safe low-scope execution -> `18_ASSISTED_EXECUTION_LOW_SCOPE.md`;
- chunk validation details -> `WELDING_CHUNK_VALIDATION_RULES.md`;
- meta-governance and drift control -> `20_RULES_GOVERNANCE.md`.

If a new rule spans multiple documents, write it once in the owner document and reference it elsewhere instead of duplicating.

---

## 12. Overengineering control

A rule is overengineered if it adds process without reducing risk.

Warning signs:

- new document for a one-line correction;
- repeated rules across files;
- blocking low-scope reversible work without critical uncertainty;
- adding fields that the loader does not use and humans will not review;
- requiring validation unavailable in the current environment without a fallback;
- creating more governance than execution.

If overengineering is detected:

```text
prefer smaller rule, smaller scope, or POST_ACTION_REVIEW instead of new process
```

---

## 13. Final operating rule

Governance exists to keep the system safe and moving.

It must prevent chaos, not create paralysis.

Default operating principle:

```text
block high-risk uncertainty, condition medium-risk change, and allow low-scope reversible progress with validation.
```

If a rule cannot support that principle, it must be revised or deprecated.
