# 14_P2_FUNCTIONAL_VALIDATION

## Objetivo

Validar funcionalmente que el RAG HOT responde usando los tres chunks curados principales:

```text
baseline criteria -> KQL window/std pattern -> HOT architecture
```

---

## Prueba ejecutada

Pregunta:

```text
Explica brevemente como usar std_RD_actual y std_RD_baseline para vigilar inestabilidad RD por RobotId y ProgramId?
```

---

## Resultado de recuperación

Fuentes recuperadas:

```text
1. fabric_kql_rd_baseline_criteria_001
   score aprox: 58.03

2. fabric_kql_rd_window_std_001
   score aprox: 48.20

3. fabric_rti_operations_accelerator_001
   score aprox: 31.23
```

Conclusión:

```text
La recuperación RAG/BM25 es correcta.
```

---

## Resultado de respuesta

La respuesta fue breve y usó el enfoque correcto:

- compara `std_RD_actual` contra `std_RD_baseline`;
- habla de ventana temporal;
- respeta `RobotId` y `ProgramId`;
- no mezcla robots o programas distintos;
- indica ajuste posterior según eventos de calidad.

---

## Problema pendiente

La respuesta perdió el valor numérico del umbral:

```text
std_RD_actual > std_RD_baseline * .
```

Debe conservar:

```text
std_RD_actual > std_RD_baseline * 1.5
```

---

## Decisión

P2 queda en estado:

```text
PARCIAL
```

La recuperación es válida, pero la respuesta funcional todavía no cumple el criterio de conservar constantes técnicas.

---

## Hipótesis

El problema no parece estar en BM25 ni en los chunks recuperados, sino en la generación del modelo Ollama o en cómo el contexto expone el valor `1.5`.

---

## Siguiente acción recomendada

Antes de seguir ampliando el RAG, revisar el chunk `fabric_kql_rd_baseline_criteria_001.json` para asegurar que la regla aparece de forma explícita, repetida y fácil de recuperar literalmente:

```text
Regla literal: std_RD_actual > std_RD_baseline * 1.5
```

No tocar todavía servicios, tokens ni arquitectura RAG.
