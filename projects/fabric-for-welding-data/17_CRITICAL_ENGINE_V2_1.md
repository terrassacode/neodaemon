# CRITICAL_ENGINE_V2_1

Status: official operational skill definition  
Scope: OpenClaw RAG Welding System, RD interpretation, HOT process-stability work and controlled automation decisions  
Version: v2.1

---

## 1. Purpose

CRITICAL_ENGINE_V2_1 is an operational control skill.

Its purpose is not to answer better. Its purpose is to prevent incorrect decisions before they are executed, while still preserving controlled forward progress.

It must detect structural errors, unsafe assumptions, weak validation, RAG contamination risk and incorrect technical interpretation before any relevant action is approved.

Core rule:

```text
CRITICAL_ENGINE_V2_1 must never leave the system without an executable next step.
```

Every evaluation must end with:

```text
SIGUIENTE PASO PROPUESTO
```

---

## 2. Mandatory invocation

CRITICAL_ENGINE_V2_1 must be invoked before any relevant decision involving:

- creating chunks;
- modifying chunks;
- changing RAG rules;
- changing RAG prompts;
- touching loader, retriever or filter logic;
- touching `api_rag_v2.py`;
- interpreting RD or welding technical signals;
- defining baseline criteria;
- creating automation;
- activating PDF ingestion;
- generating chunks at scale;
- using RAG output for operational or automatic decisions.

If CRITICAL_ENGINE_V2_1 is not invoked before such an action, the action is considered invalid.

Recommended order:

```text
CRITICAL_ENGINE_V2_1 -> TASK_VALIDATOR -> minimal execution -> validation
```

---

## 3. Authority

CRITICAL_ENGINE_V2_1 can:

- block execution;
- require additional validation;
- downgrade a decision to experimental;
- force a smaller pilot scope;
- require rollback planning;
- require human confirmation;
- mark an action as unsafe for RAG quality;
- require separation between rule, limitation, query, example and answer contract.

It cannot be ignored without explicit justification.

If it returns `BLOQUEAR`, execution must not proceed until the blocking issues are resolved or Albert explicitly overrides with a documented reason.

---

## 4. Uncertainty classification

Every uncertainty must be classified as either critical or tolerable.

### 4.1 Critical uncertainty

Critical uncertainty blocks execution.

Examples:

- unknown loader contract;
- unknown chunk folder;
- unknown text field used by the loader;
- risk of corrupting RAG behaviour;
- risk of touching tokens or configuration;
- risk of changing gateway, Telegram or services unintentionally;
- impossible validation;
- no rollback path;
- unclear source of technical claim;
- format incompatible with current RAG loader;
- action could cause RD to be interpreted as a final quality diagnosis;
- action could make provisional rules appear definitive.

Rule:

```text
critical uncertainty -> VEREDICTO = BLOQUEAR
```

### 4.2 Tolerable uncertainty

Tolerable uncertainty does not block if the action is controlled, reversible and validated.

Examples:

- imperfect granularity, such as uncertain `ID_SW` availability;
- provisional thresholds;
- incomplete production dataset;
- controlled hypotheses;
- pilot chunks clearly marked as review;
- validation by BM25 before scaling;
- no runtime changes;
- rollback available.

Rule:

```text
tolerable uncertainty -> VEREDICTO may be CONDICIONADO + piloto
```

---

## 5. Impact scope

Every evaluation must classify impact scope.

```text
impact_scope: low | medium | high
```

### 5.1 low

Low impact means a controlled experiment or documentation-only change.

Examples:

- one pilot chunk;
- one Markdown rule update;
- read-only inspection;
- BM25-only validation;
- reversible change without runtime impact.

Rule:

```text
low -> favor controlled progress
```

If there is no critical P0, rollback exists and validation is possible, the verdict cannot be `BLOQUEAR`.

It must be:

```text
CONDICIONADO + piloto
```

or:

```text
AUTORIZAR
```

### 5.2 medium

Medium impact affects RAG behaviour or the interpretation layer.

Examples:

- several operational chunks;
- answer contract chunks;
- RAG prompt change;
- validation rules used for chunk creation;
- changes likely to influence retrieval results.

Rule:

```text
medium -> normally CONDICIONADO
```

Requires explicit validation before and after execution.

### 5.3 high

High impact affects the runtime system.

Examples:

- loader changes;
- retriever changes;
- filter changes;
- `api_rag_v2.py` changes;
- service restart;
- gateway changes;
- Telegram routing;
- tokens or configuration;
- active automation.

Rule:

```text
high -> maximum validation and explicit human authorization
```

---

## 6. Anti-paralysis rule

CRITICAL_ENGINE_V2_1 must block real structural risk, but it must not freeze low-risk work.

If all conditions are true:

- no critical P0 exists;
- `impact_scope = low`;
- rollback exists;
- validation is possible;
- action is limited to a pilot or documentation-only step;

then:

```text
VEREDICTO cannot be BLOQUEAR
```

The correct verdict is:

```text
CONDICIONADO + piloto
```

The output must include a concrete, executable next step.

---

## 7. Mandatory output format

Every CRITICAL_ENGINE_V2_1 evaluation must use this structure:

```text
P0 — BLOQUEOS ESTRUCTURALES
...

P1 — RIESGOS CRÍTICOS
...

P2 — RIESGOS DE CALIDAD
...

P3 — MEJORAS
...

CONTRADICCIONES
...

INCERTIDUMBRE
- crítica:
- tolerable:

IMPACT_SCOPE
low | medium | high

VALIDACIONES REQUERIDAS
...

VEREDICTO
BLOQUEAR | CONDICIONADO + piloto | CONDICIONADO | AUTORIZAR

SIGUIENTE PASO PROPUESTO
...
```

No evaluation is complete without `SIGUIENTE PASO PROPUESTO`.

---

## 8. Specific rules for OpenClaw RAG + RD

CRITICAL_ENGINE_V2_1 must detect and report:

- RD used as a final quality diagnosis;
- RD used as direct nugget prediction without evidence;
- confusion between signal, cause, defect and action;
- chunks that are too long or mix multiple concepts;
- missing useful BM25 keywords;
- keywords and query patterns present only as JSON fields, not embedded in `text` or `content`;
- differences between `text` and `content`;
- reliance on fields not actively used by the current loader;
- assuming `quality_score` filters retrieval;
- assuming `validation` or `status` filters retrieval;
- provisional factor `1.5` becoming a fixed rule;
- invented variables such as `RD_factor`;
- invented KQL;
- lack of language normalization;
- mixing `RobotId` and `ProgramId` groups;
- using `ID_SW` without sufficient traceability;
- missing source;
- missing applicability;
- missing risk note;
- lack of rollback;
- lack of validation.

---

## 9. Operational loader compatibility awareness

CRITICAL_ENGINE_V2_1 must evaluate chunk proposals against the current loader contract.

Current confirmed loader behaviour:

- chunks are loaded from `/openclaw/workspace/main/rag_store/chunks_v2`;
- the loader reads `text` or `content`;
- if both exist, `text` has priority;
- the loader preserves `source`, `url` and `chunk_id`;
- the retriever may return `block_type`, `title` and `quality_score`;
- `keywords`, `query_patterns`, `validation`, `status`, `applicability` and `risk_note` are not directly used by BM25 if they exist only as JSON fields;
- for BM25 to use keywords or query patterns, they must also be embedded inside `text` or `content` in readable form;
- `load_chunks()` is called on each question; no cache is currently confirmed.

Operational consequence:

```text
P2B chunks must include both text and content, with the same main content.
```

---

## 10. Correct validation/status mapping

Allowed status values:

```text
draft
review
approved
quarantine
deprecated
```

Correct mapping:

| validation | status      | meaning |
|------------|-------------|---------|
| A          | approved    | validated and usable |
| B          | review      | valid but conditioned or requiring validation |
| C          | quarantine  | doubtful; not for direct use |
| D          | deprecated  | discarded, obsolete or unsafe |

Additional usage:

- `draft` may be used for work in progress that is not ready for operational RAG use.
- `review` replaces the older invalid status `conditioned`.
- `conditioned` is not an allowed status.

Detection rule:

```text
If status = conditioned, report CONTRADICCIÓN and require correction to status = review when validation = B.
```

---

## 11. Verdict rules

### BLOQUEAR

Use when:

- critical uncertainty exists;
- impact is high and validation/rollback is missing;
- loader contract is unknown;
- action risks corrupting RAG;
- action risks touching tokens/config/services unexpectedly;
- output cannot be validated;
- chunk format is incompatible;
- RD is used as a definitive quality diagnosis;
- provisional rules are presented as final.

### CONDICIONADO + piloto

Use when:

- no critical P0 exists;
- impact is low;
- rollback exists;
- validation is possible;
- uncertainty is tolerable;
- action can be limited to one pilot or one document.

### CONDICIONADO

Use when:

- impact is medium;
- risks are manageable;
- validation must happen before/after execution;
- execution should be limited and reversible.

### AUTORIZAR

Use when:

- no critical uncertainty exists;
- risks are low;
- validation exists;
- rollback exists if modification is involved;
- scope is clear and constrained.

---

## 12. Example applied to P2B

Input:

```text
Create manual P2B chunks about RD and HOT baseline.
```

### P0 — BLOQUEOS ESTRUCTURALES

No critical P0 if the action is reduced to one pilot chunk and all of the following are true:

- the chunk includes both `text` and `content`;
- `text` and `content` contain the same main content;
- keywords are embedded inside `text` or `content`;
- query patterns are embedded inside `text` or `content`;
- `validation = B`;
- `status = review`;
- `risk_note` exists;
- JSON validation is possible;
- BM25 validation is possible;
- rollback exists;
- no runtime file is touched.

If the proposal is to create many chunks without pilot validation, P0 exists and the action must be blocked or reduced to pilot.

### P1 — RIESGOS CRÍTICOS

- The factor `1.5` may become dogma.
- RD may be described as final quality diagnosis.
- BM25 may fail if useful terms are not embedded in text/content.
- `validation` and `status` do not filter retrieval in the current loader.
- KQL may be invented if not explicitly curated.

### P2 — RIESGOS DE CALIDAD

- Chunk too long.
- Too many ideas in one chunk.
- Spanish/English terminology not normalized.
- Baseline chunks over-retrieved for unrelated questions.
- Missing negative examples.

### P3 — MEJORAS

- Start with one negative guardrail chunk.
- Keep text short.
- Include synonyms: `RD`, `resistencia dinámica`, `dynamic resistance`.
- Include query patterns in readable form inside `text` and `content`.
- Add `applicability` and `risk_note`.

### CONTRADICCIONES

- Documentation may include structured fields that BM25 does not use directly.
- Current loader prioritizes `text`, while older rules emphasized `content`.
- Correct approach: include both `text` and `content`, aligned.
- `status = conditioned` is invalid; use `status = review` for `validation = B`.

### INCERTIDUMBRE

Critical:

- none if limited to one pilot chunk and validation is possible.

Tolerable:

- incomplete production dataset;
- uncertain `ID_SW` availability;
- provisional threshold `1.5`;
- mapping of real plant column names pending.

### IMPACT_SCOPE

```text
low
```

Reason:

- one pilot chunk;
- reversible;
- no runtime modification;
- no service restart;
- validation possible.

### VALIDACIONES REQUERIDAS

- JSON valid.
- `text` present.
- `content` present.
- `text` and `content` aligned.
- keywords embedded inside `text` or `content`.
- query patterns embedded inside `text` or `content`.
- if `1.5` appears, `provisional` must also appear.
- if `nugget` appears, `no predice` or equivalent warning must also appear.
- BM25 returns the pilot chunk for expected queries.

### VEREDICTO

```text
CONDICIONADO + piloto
```

### SIGUIENTE PASO PROPUESTO

Create one pilot chunk only:

```text
fabric_rd_no_nugget_prediction_001.json
```

Purpose:

```text
Clarify that RD / resistencia dinámica / dynamic resistance is a process signal for stability monitoring, not direct nugget prediction and not a final weld-quality guarantee.
```

Required fields:

- `chunk_id`
- `block_type`
- `title`
- `text`
- `content`
- `source`
- `url`
- `quality_score`
- `keywords`
- `query_patterns`
- `validation = B`
- `status = review`
- `applicability`
- `risk_note`

Do not create a batch of chunks until the pilot passes validation.

---

## 13. Change log

- v2.1: Added anti-paralysis rule, impact scope, uncertainty classification and corrected validation/status mapping. `status = conditioned` removed; `validation = B` now maps to `status = review`.
