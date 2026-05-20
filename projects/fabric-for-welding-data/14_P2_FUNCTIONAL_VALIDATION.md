# 14_P2_FUNCTIONAL_VALIDATION

## Objetivo

Validar funcionalmente que el RAG HOT responde usando los tres chunks curados principales:

```text
baseline criteria -> KQL window/std pattern -> HOT architecture
```

---

## Prueba ejecutada con wrapper

Wrapper usado:

```text
scripts/rag_ops/rag_query_local.sh
```

Pregunta:

```text
Como comparar std_RD_actual con std_RD_baseline en soldadura?
```

La query fue codificada correctamente y el token quedó sanitizado como:

```text
token=<REDACTED>
```

---

## Resultado de recuperación

Fuentes recuperadas:

```text
1. fabric_kql_rd_baseline_criteria_001
   score aprox: 39.43

2. fabric_kql_rd_window_std_001
   score aprox: 25.89

3. fabric_rti_operations_accelerator_001
   score aprox: 24.02
```

Conclusión:

```text
La recuperación RAG/BM25 es correcta.
```

---

## Resultado de respuesta

La respuesta fue funcionalmente mejor que en pruebas anteriores:

- usa los chunks correctos;
- mantiene el enfoque de comparar `std_RD_actual` contra `std_RD_baseline`;
- menciona ventana temporal, `RobotId` y `ProgramId`;
- indica que el criterio debe validarse con datos reales;
- no imprime el token;
- no genera una query KQL larga rota.

---

## Problemas pendientes

La respuesta todavía presenta dos problemas:

### 1. Pierde el valor numérico del umbral

Salida observada:

```text
std RD_baseline * .
```

Debe conservar:

```text
std_RD_baseline * 1.5
```

### 2. Degrada nombres técnicos

Ejemplos observados:

```text
std RD actual
std RD baseline
```

Debe conservar:

```text
std_RD_actual
std_RD_baseline
```

---

## Decisión

P2 queda en estado:

```text
PARCIAL
```

La recuperación es válida y el wrapper funciona, pero la respuesta funcional todavía no cumple el criterio de conservar constantes y nombres técnicos.

---

## Diagnóstico

El problema no está en:

- el wrapper;
- el token;
- BM25;
- la recuperación de chunks.

El problema está en la capa de generación/postprocesado y/o en la forma en que el chunk expone literalmente la regla.

---

## Siguiente acción recomendada

No ampliar el RAG todavía.

Antes de cerrar P2, reforzar el chunk `fabric_kql_rd_baseline_criteria_001.json` para que incluya de forma literal y destacada:

```text
Regla literal: std_RD_actual > std_RD_baseline * 1.5
```

También debe indicar explícitamente:

```text
No cambiar nombres técnicos como std_RD_actual o std_RD_baseline.
```

Después repetir prueba con `rag_query_local.sh`.
