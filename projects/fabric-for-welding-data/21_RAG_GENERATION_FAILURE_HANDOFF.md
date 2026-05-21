# 21_RAG_GENERATION_FAILURE_HANDOFF.md

Status: paused / handoff
Scope: OpenClaw RAG Welding System
Date: 2026-05-21

---

## 1. Purpose

This document freezes the current RAG work and records the exact state reached before pausing.

The RAG chunk pipeline is not considered failed. Retrieval and preflight validation work correctly.

The current blocker is the final generated answer produced by `/rag-ask`.

---

## 2. Current decision

Do not create more chunks.

Do not start PDF ingestion.

Do not promote pilot chunks to `approved`.

Do not modify runtime yet.

Next future work must diagnose answer generation, prompt handling and post-processing before expanding the corpus.

---

## 3. What is working

The following components are working:

- `WELDING_CHUNK_VALIDATION_RULES.md` v0.2
- `CRITICAL_ENGINE_V2_1`
- `ASSISTED_EXECUTION_LOW_SCOPE`
- `20_RULES_GOVERNANCE.md`
- `rag_chunk_preflight.sh`
- BM25 retrieval tests
- manual pilot chunk workflow

Three pilot chunks were created locally and validated:

```text
fabric_rd_no_nugget_prediction_001
fabric_rd_process_stability_signal_001
fabric_rd_baseline_robot_program_001
```

Their intended roles:

```text
chunk 1 = negative guardrail: RD does not predict nugget by itself
chunk 2 = positive use: RD as process stability signal
chunk 3 = method rule: baseline by RobotId + ProgramId
```

All three passed:

- JSON validation
- pilot preflight
- BM25 intent checks

---

## 4. What failed

The `/rag-ask` generated answer is not reliable yet.

Observed issues:

1. It invented unsupported content:

```text
tendencia a la corrosión
```

2. It produced broken/truncated output:

```text
std_RD_baseli
std_RD_actual > std_RD_baseline * .
robot, robot
```

3. It sometimes sounded too certain:

```text
variabilidad anómala
```

Preferred wording should be conditional:

```text
puede indicar variabilidad o posible inestabilidad
```

---

## 5. Retrieval-only diagnosis

A read-only debug wrapper was created locally:

```text
/openclaw/workspace/main/context_repo/scripts/rag_ops/rag_query_debug_context.sh
```

It performs retrieval-only diagnosis:

- no Ollama
- no `/rag-ask`
- no writes
- prints query, chunks, scores and snippets
- searches `chunks_v2` for problematic terms

The debug run showed:

### 5.1 Corrosion was not in the corpus

```text
corrosion = 0 matches
corrosión = 0 matches
```

Conclusion:

```text
"tendencia a la corrosión" was likely LLM invention, not retrieved context.
```

### 5.2 The `1.5` rule exists in older chunks

Matches found in:

```text
fabric_kql_rd_baseline_criteria_001.json
fabric_rd_baseline_answer_contract_001.json
```

Those chunks contain or reference:

```text
std_RD_actual > std_RD_baseline * 1.5
```

They mark `1.5` as provisional, but generation produced the broken form:

```text
std_RD_actual > std_RD_baseline * .
```

Conclusion:

```text
The source context contains the formula, but generation or post-processing is corrupting it.
```

### 5.3 Query 2 retrieved an older/non-pilot chunk first

For query:

```text
como analizar estabilidad RD por robot
```

The top result was:

```text
fabric_rti_operations_accelerator_001
```

not the pilot stability chunk.

Conclusion:

```text
Retrieval ranking still allows older chunks to dominate some general RD questions.
```

---

## 6. Likely root causes

Likely causes, in order:

1. Prompt is too permissive or not strict enough about using only context.
2. `clean_answer()` or other post-processing may corrupt text, variables or formulas.
3. Older chunks with `1.5` and baseline answer contracts are being retrieved.
4. LLM hallucination still occurs when context is incomplete or mixed.
5. Pilot chunks are not the main problem.

---

## 7. Current blocker

The blocker is not chunk creation.

The blocker is:

```text
BM25 retrieval works, but final answer generation is not yet trustworthy.
```

Therefore:

```text
BLOCK new chunks
BLOCK PDF ingestion
BLOCK chunk approval
BLOCK any industrial decision based on /rag-ask output
```

---

## 8. Future next step

The next safe step, when work resumes, is read-only inspection of:

```text
/openclaw/api_rag_v2.py
```

Focus areas:

- prompt template
- context assembly
- `clean_answer()`
- `remove_prefix_fragments()`
- formula preservation
- rule preventing unsupported additions
- behavior when retrieved context is mixed

Do not modify `api_rag_v2.py` directly without:

1. CRITICAL_ENGINE_V2_1 review
2. TASK_VALIDATOR
3. backup
4. diff
5. rollback plan
6. controlled test

---

## 9. Future diagnostic commands

Use retrieval-only first:

```bash
bash /openclaw/workspace/main/context_repo/scripts/rag_ops/rag_query_debug_context.sh "RD alta significa mala soldadura?"

bash /openclaw/workspace/main/context_repo/scripts/rag_ops/rag_query_debug_context.sh "como analizar estabilidad RD por robot"

bash /openclaw/workspace/main/context_repo/scripts/rag_ops/rag_query_debug_context.sh "std_RD_actual alto que significa"
```

Do not run more `/rag-ask` tests until prompt/post-processing has been reviewed.

---

## 10. Open items

Open:

- version `rag_query_debug_context.sh` if still uncommitted
- inspect `api_rag_v2.py` read-only
- decide whether older chunks with `1.5` should be revised, isolated or kept
- improve prompt to reject unsupported statements
- protect formulas from post-processing corruption
- rerun controlled `/rag-ask` test after correction

Closed:

- chunk validation rules v0.2
- loader compatibility documentation
- CRITICAL_ENGINE_V2_1
- assisted low-scope execution policy
- rules governance
- pilot preflight wrapper
- three pilot chunks validated with BM25

---

## 11. Final note

This pause is intentional.

The system is in a good state for retrieval and governance, but not yet for generated technical answers.

The correct next work is diagnosis and hardening of the generation layer, not adding more knowledge.
