# WELDING_CHUNK_VALIDATION_RULES.md

Version: v0.2  
Scope: RAG technical chunks for spot welding, dynamic resistance (RD) and HOT process-stability analysis  
Status: official validation rules before PDF extraction

---

## 1. Purpose

This document defines the validation contract for technical chunks used by the OpenClaw RAG Welding System.

The goal is to prevent generic, unsafe, overconfident or poorly sourced answers when interpreting spot welding data, especially dynamic resistance (RD), process stability, robot/program behaviour, baseline comparison and quality-related signals.

No PDF extraction, chunk generation, bulk ingestion or RAG expansion should start before these rules are respected.

---

## 2. Base chunk schema

Every technical chunk must keep a stable base schema. The schema is intentionally explicit so that each chunk can be reviewed before it is allowed to influence RAG answers.

```json
{
  "chunk_id": "",
  "topic": "",
  "subtopic": "",
  "title": "",
  "content": "",
  "keywords": [],
  "query_patterns": [],
  "source": "",
  "page": null,
  "layer": "",
  "type": "signal | cause | defect | action | limitation | context | definition | rule | query_pattern",
  "validation": "A | B | C | D",
  "status": "approved | conditioned | quarantine | discarded",
  "applicability": "",
  "risk_note": "",
  "validation_note": ""
}
```

Required fields:

- `chunk_id`
- `topic`
- `title`
- `content`
- `source`
- `type`
- `validation`
- `status`
- `applicability`
- `risk_note`

Rules:

- `chunk_id` must be stable and unique.
- `content` must be short, technical and directly useful.
- `source` must allow traceability to the origin of the claim.
- `validation` and `status` must follow the status contract below.
- `risk_note` must explain the main misuse risk.

---

## 3. Optional recommended fields

The following fields are recommended when they improve retrieval, review or traceability:

```json
{
  "document_id": "",
  "source_title": "",
  "source_url": "",
  "section": "",
  "page_range": "",
  "equipment_scope": "",
  "process_scope": "",
  "variables": [],
  "requires_fields": [],
  "forbidden_inference": [],
  "related_chunks": [],
  "review_owner": "",
  "review_date": "",
  "version": "v0.2"
}
```

Recommended use:

- Use `variables` for literal technical names such as `std_RD_actual`, `std_RD_baseline`, `avg_RD`, `RobotId`, `ProgramId` or `ID_SW`.
- Use `requires_fields` when a rule only works if certain columns or identifiers exist.
- Use `forbidden_inference` to block unsafe conclusions such as predicting nugget quality from RD alone.
- Use `related_chunks` to link rules, examples and limitations without duplicating content.

---

## 4. Validation levels

Validation levels classify how reliable and directly usable a chunk is.

They are not a generic quality label for the source alone. They describe whether the chunk can safely guide RAG answers.

Use the most conservative level when evidence is incomplete.

---

## 5. A — valid and reliable

Use level **A** only when the chunk is technically clear, traceable and safe to use directly.

Criteria:

- The statement is supported by a reliable source or by a validated internal rule.
- The scope is explicit.
- The chunk does not overclaim causality.
- The chunk does not imply final weld quality from RD alone.
- The chunk distinguishes observation, interpretation and action.
- The chunk can be used in RAG answers without extra warning beyond normal context.

Typical examples:

- RD is a process signal in spot welding.
- `std_RD_actual` can be compared with `std_RD_baseline` for process-stability monitoring.
- Baseline comparison should be made by `RobotId + ProgramId`, and optionally `ID_SW` if traceability is sufficient.
- The rule `std_RD_actual > std_RD_baseline * 1.5` is an initial criterion to validate with real data, not a fixed truth.

Allowed status:

```json
{
  "validation": "A",
  "status": "approved"
}
```

---

## 6. B — valid but conditioned

Use level **B** when the chunk is useful but depends on explicit conditions.

Criteria:

- The rule is plausible but context-dependent.
- The chunk requires plant-specific validation.
- The statement depends on sampling, traceability, sensor reliability, process window, robot, program, product family or dataset structure.
- The chunk can be used by the RAG only if the condition is attached to the answer.

Typical examples:

- A threshold is proposed but not yet validated on real production data.
- A KQL pattern is structurally valid but column names may differ by dataset.
- `ID_SW` granularity is recommended only if the system has stable point-level traceability.
- A correlation with defects is suggested but not confirmed as causal.

Allowed status:

```json
{
  "validation": "B",
  "status": "conditioned"
}
```

RAG answer rule:

- Mention the condition explicitly.
- Do not present B-level content as a definitive rule.
- If the condition is not met, explain the criterion without overclaiming.

---

## 7. C — doubtful / quarantine

Use level **C** when the chunk may contain useful information but is incomplete, ambiguous or insufficiently supported.

Criteria:

- The source is unclear or weak.
- The page, section or extraction context is missing.
- The wording is too generic.
- The chunk mixes multiple ideas without clear separation.
- The claim may be true but lacks enough evidence for direct use.
- The chunk risks encouraging unsafe interpretation of RD, process stability or quality.

Allowed status:

```json
{
  "validation": "C",
  "status": "quarantine"
}
```

RAG answer rule:

- Do not use C chunks for direct recommendations.
- Use only as internal review material.
- Prefer A or B chunks when available.

---

## 8. D — discarded

Use level **D** when the chunk should not be used by the RAG.

Criteria:

- The chunk is wrong, obsolete, duplicated without value, misleading or unsafe.
- It invents variables, thresholds, tables, columns or causal links.
- It implies nugget quality prediction without evidence.
- It mixes robots, programs or welding points in a way that invalidates the analysis.
- It contains untraceable claims from uncontrolled extraction.
- It contains sensitive data, tokens, credentials or private plant information.

Allowed status:

```json
{
  "validation": "D",
  "status": "discarded"
}
```

RAG answer rule:

- D chunks must not be indexed for answers.
- If already indexed, they must be removed or filtered before use.

---

## 9. Status contract

The `validation` and `status` fields must remain coherent.

Allowed combinations:

| validation | status      | Meaning |
|------------|-------------|---------|
| A          | approved    | Directly usable |
| B          | conditioned | Usable only with explicit condition |
| C          | quarantine  | Keep for review, not direct answer |
| D          | discarded   | Do not use |

Forbidden combinations:

- `validation: A` with `status: quarantine`
- `validation: D` with `status: approved`
- empty `validation`
- empty `status`
- undocumented custom status values

If uncertainty exists, use:

```json
{
  "validation": "C",
  "status": "quarantine"
}
```

---

## 10. Transversal rules

These rules apply to all chunks regardless of topic.

### 10.1 Do not overclaim RD

RD is a process signal, not a standalone proof of final weld quality.

Allowed:

- RD can support process-stability monitoring.
- RD variability can indicate possible instability.
- RD should be interpreted with robot, program, welding point and process context.

Forbidden:

- RD alone proves nugget size.
- RD alone confirms weld quality.
- A single RD threshold is universal.

### 10.2 Preserve technical names

Do not rename validated variables.

Required names must remain literal when present:

- `std_RD_actual`
- `std_RD_baseline`
- `avg_RD`
- `RobotId`
- `ProgramId`
- `ID_SW`

Forbidden:

- inventing `RD_factor`
- replacing `std_RD_actual` with vague names like “current deviation factor”
- changing baseline variable names without a curated mapping

### 10.3 Do not invent KQL

KQL can be included only when the query is curated or explicitly marked as illustrative.

If there is no curated query:

- explain the criterion without code;
- do not invent table names;
- do not invent column names;
- do not invent thresholds.

### 10.4 Keep robot/program separation

Do not mix robots or programs when defining baselines unless the chunk explicitly validates that aggregation.

Default baseline level:

```text
RobotId + ProgramId
```

Optional finer level:

```text
RobotId + ProgramId + ID_SW
```

Use `ID_SW` only if traceability is reliable enough.

### 10.5 Mark provisional thresholds

Any threshold not validated with real production data must be marked as provisional.

Example:

```text
std_RD_actual > std_RD_baseline * 1.5
```

This is an initial criterion to validate with real data, not a fixed universal truth.

### 10.6 Separate monitoring from prediction

A stability rule is not a nugget prediction model.

Allowed:

- “This is a process-stability monitoring layer.”
- “This can feed dashboards and alerts.”

Forbidden:

- “This predicts nugget.”
- “This guarantees weld quality.”

### 10.7 Keep answers short and grounded

Chunks should help the RAG answer briefly, technically and with source discipline.

Avoid:

- marketing language;
- generic industrial examples unrelated to welding;
- unsupported causal claims;
- long mixed paragraphs with multiple unrelated claims.

---

## 11. Final guardrails before PDF extraction

Before extracting PDFs or generating chunks at scale, verify:

1. The target topic is explicitly defined.
2. The extraction does not create chunks without source/page traceability.
3. Every chunk has `validation`, `status`, `applicability` and `risk_note`.
4. RD is treated as a process signal, not as a standalone quality verdict.
5. Thresholds are marked as provisional unless validated with real data.
6. KQL is not generated unless curated.
7. Technical names are preserved exactly.
8. `RobotId + ProgramId` separation is preserved for baselines.
9. `ID_SW` is used only when traceability is sufficient.
10. C and D chunks are not used for direct RAG answers.
11. No tokens, credentials, internal secrets or sensitive plant data are included.
12. A small pilot batch must be reviewed before any massive chunk generation.

If any guardrail fails, stop extraction and quarantine the affected material.

---

## 12. Minimal approved example

```json
{
  "chunk_id": "rd_baseline_rule_001",
  "topic": "resistencia_dinamica",
  "subtopic": "baseline_estabilidad",
  "title": "Comparación de std_RD_actual contra std_RD_baseline",
  "content": "Para vigilancia de estabilidad del proceso, comparar std_RD_actual contra std_RD_baseline por RobotId + ProgramId. Una regla inicial es std_RD_actual > std_RD_baseline * 1.5, pero el factor 1.5 es provisional y debe validarse con datos reales. Esta regla no predice nugget; sirve como capa previa de vigilancia.",
  "keywords": ["std_RD_actual", "std_RD_baseline", "RobotId", "ProgramId", "RD", "baseline"],
  "query_patterns": ["comparar std_RD_actual con std_RD_baseline", "baseline RD por robot y programa", "regla 1.5 RD"],
  "source": "internal_rules",
  "page": null,
  "layer": "process_stability_monitoring",
  "type": "rule",
  "validation": "B",
  "status": "conditioned",
  "applicability": "soldadura por puntos con trazabilidad por robot y programa",
  "risk_note": "El factor 1.5 es provisional y requiere validación con datos reales.",
  "validation_note": "No usar como predicción de nugget ni como criterio universal de calidad."
}
```

---

## 13. Change log

- v0.2: Added complete validation levels, optional recommended fields, status contract, transversal rules and final guardrails before PDF extraction.
