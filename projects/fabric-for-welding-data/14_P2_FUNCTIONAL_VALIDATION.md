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

La prueba confirma que el wrapper funciona, pero la respuesta del modelo no cumple todavía el criterio funcional.

Aspectos correctos:

- usa los chunks correctos;
- conserva parcialmente el enfoque de variabilidad RD;
- no imprime el token;
- ejecuta la consulta mediante wrapper seguro;
- no requiere comandos manuales largos.

---

## Problemas pendientes

### 1. Pierde el valor numérico del umbral

Salida observada:

```text
umbral determinado, por ejemplo, .
```

Debe conservar:

```text
1.5
```

### 2. Inventa una métrica no curada

Salida observada:

```text
RD_factor = (std_RD_actual / dispersion esperada)
```

Problema:

```text
RD_factor no forma parte del criterio curado actual.
```

### 3. Genera KQL no curado

Salida observada:

```text
SpotWeldEvents | where Timestamp > ago(h)
...
bin(Timestamp, m)
```

Problema:

```text
El modelo está generando código incompleto o no validado.
```

### 4. Degrada nombres técnicos

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
NO CERRADO
```

La recuperación es válida y el wrapper funciona, pero la respuesta funcional no es aceptable para cierre.

---

## Diagnóstico

El problema no está en:

- el wrapper;
- el token;
- BM25;
- la recuperación de chunks.

El problema está en la capa de generación y/o en que el chunk no fuerza suficientemente una respuesta literal cerrada.

---

## Siguiente acción recomendada

No ampliar el RAG todavía.

Crear o reforzar un chunk de criterio cerrado que indique explícitamente:

```text
Respuesta esperada corta:
Comparar std_RD_actual contra std_RD_baseline por RobotId + ProgramId.
Regla literal: std_RD_actual > std_RD_baseline * 1.5.
El valor 1.5 es provisional y debe validarse con datos reales.
No inventar RD_factor.
No generar KQL si no está curado.
No cambiar nombres técnicos.
```

Después repetir prueba con:

```text
rag_test_bm25.sh
rag_query_local.sh
```
