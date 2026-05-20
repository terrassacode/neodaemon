# 13_RAG_OPS_WRAPPER_VALIDATION

## Objetivo

Registrar la validación de los wrapper scripts seguros para `rag_ops_guarded`.

---

## F1 — Lectura pura

### Scripts validados

```text
scripts/rag_ops/rag_count_chunks.sh
scripts/rag_ops/rag_status_readonly.sh
```

### Resultado

- `rag_count_chunks.sh`: OK.
- `rag_status_readonly.sh`: OK.
- Servicio RAG activo.
- Salida concisa.
- Token sanitizado como `token=<REDACTED>`.
- Sin reinicios.
- Sin escritura operativa.
- Sin `/rag-ask` nuevo.

### Estado F1

```text
CERRADO
```

---

## F2 — Validación local

### Scripts validados

```text
scripts/rag_ops/rag_py_compile.sh
scripts/rag_ops/rag_test_bm25.sh
```

### Resultado py_compile

```text
STATUS=OK
RESULT=py_compile_ok
```

Archivo validado:

```text
/openclaw/api_rag_v2.py
```

### Resultado BM25

Consulta usada:

```text
baseline std_RD_actual std_RD_baseline RobotId ProgramId ID_SW media global inestabilidad
```

Resultado:

```text
CHUNKS_LOADED=40
RESULTS_RETURNED=5
RESULT_1_CHUNK_ID=fabric_kql_rd_baseline_criteria_001
RESULT_1_SCORE=51.06778529813489
RESULT_2_CHUNK_ID=fabric_kql_rd_window_std_001
RESULT_2_SCORE=27.743975848622352
RESULT_3_CHUNK_ID=fabric_rti_operations_accelerator_001
RESULT_3_SCORE=8.351998375156162
```

### Conclusión F2

La validación local funciona sin Ollama, sin token y sin `/rag-ask`.

La recuperación BM25 mantiene la cadena correcta:

```text
baseline criteria -> KQL window/std pattern -> HOT architecture
```

### Estado F2

```text
CERRADO
```

---

## Riesgos pendientes detectados

| Riesgo | Estado |
|---|---|
| Token visible en logs históricos del servicio | pendiente P10 |
| Ruido secundario BM25 por chunks antiguos | pendiente P7 |
| Calidad de generación Ollama | P1 mitigado, no perfecto |
| Acciones con token o reinicio | no implementadas todavía |

---

## Siguiente fase posible

F3 — Acciones autorizadas:

```text
rag_restart_authorized.sh
rag_query_local.sh
```

Recomendación: no implementar F3 hasta decidir si realmente es necesaria antes de P2.
