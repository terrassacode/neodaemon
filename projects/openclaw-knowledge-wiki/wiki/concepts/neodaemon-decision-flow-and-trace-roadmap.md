# Neodaemon Decision Flow & Trace Roadmap

## Estado

Roadmap creado.

## Propósito

Definir cómo toma decisiones Neodaemon y cómo dichas decisiones pueden auditarse posteriormente.

Este documento integra:

- CONTEXT_BUDGET;
- DEPENDENCY_CHECKER;
- TASK_VALIDATOR;
- RUNNER.

No redefine estos componentes.

Describe únicamente cómo colaboran.

## Problema que resuelve

Actualmente existen múltiples mecanismos de validación y control.

Sin un flujo común existe riesgo de:

- duplicación de validaciones;
- consumo innecesario de contexto;
- decisiones difíciles de auditar;
- comportamientos inconsistentes.

Además, el crecimiento de la documentación puede provocar un aumento innecesario del contexto cargado.

## Principio central

Neodaemon debe:

```text
decidir con el mínimo contexto suficiente
```

y producir una:

```text
DECISION_TRACE
```

visible y auditable.

## Objetivos

- unificar el flujo de decisión;
- reducir consumo de contexto;
- evitar validaciones redundantes;
- facilitar auditoría posterior;
- permitir crecimiento controlado del sistema.

## Principios estratégicos

### Shell First

Priorizar herramientas deterministas cuando sea posible.

Ejemplos:

```text
grep
find
git
systemctl
```

### Model On Demand

Usar razonamiento únicamente cuando sea necesario.

### Summary First

Utilizar canonical summaries antes que documentos completos.

### Source On Demand

Cargar documentos fuente únicamente cuando el summary sea insuficiente.

### Source Wins

Ante conflicto:

```text
source_doc > summary_doc
```

### Explicit Trace

Toda decisión debe generar una traza visible.

### No Recursion

Los componentes de validación no deben invocarse recursivamente.

## Alcance

Define:

- flujo de decisión;
- flujo de contexto;
- reglas de auditoría;
- interacción entre componentes.

## Fuera de alcance

No implementa:

- código;
- servicios;
- OAuth;
- gateway;
- infraestructura.

Es un documento arquitectónico.

## Flujo mínimo de decisión

Toda decisión debe seguir el mismo flujo base.

```text
REQUEST
    ↓
MODEL CHECK
    ↓
CONTEXT BUDGET
    ↓
CONTEXT LOADING
    ↓
DEPENDENCY_CHECKER (si aplica)
    ↓
TASK_VALIDATOR
    ↓
ALLOW / REVIEW / BLOCK
    ↓
RUNNER (solo ALLOW)
    ↓
DECISION_TRACE
```

## Model Check

Antes de usar razonamiento debe determinarse si la tarea puede resolverse mediante herramientas deterministas.

Ejemplos:

```text
grep
find
git
systemctl
```

Resultado:

```text
model_required = YES/NO
```

## Context Budget

Antes de cargar contexto debe asignarse un presupuesto.

Niveles:

```text
LOW
MEDIUM
HIGH
CRITICAL
```

Regla:

```text
presupuesto antes que contexto
```

## Context Loading

Regla principal:

```text
summary first
source on demand
```

Flujo:

```text
buscar summary
      ↓
cargar summary
      ↓
¿es suficiente?
      ↓
SI → continuar
NO → source_doc
```

## Escalado de contexto

Solo debe producirse cuando exista:

- incertidumbre;
- conflicto;
- riesgo elevado;
- información insuficiente.

No debe escalarse contexto simplemente porque exista documentación disponible.

## Canonical Summary Lifecycle

Los summaries permiten reducir consumo de contexto.

No sustituyen al documento fuente.

### Creación

Modelo recomendado:

```text
hybrid
```

Neodaemon propone.

Humano valida.

### Estados

```text
FRESH
STALE
DEPRECATED
```

### Invalidación

Si cambia el documento fuente:

```text
summary_status = STALE
```

hasta revisión.

### Autoridad

Siempre:

```text
source_doc > summary_doc
```

Un summary `STALE` no debe utilizarse como única fuente para decisiones:

```text
HIGH
CRITICAL
```

## Cuándo usar DEPENDENCY_CHECKER

`DEPENDENCY_CHECKER` no debe ejecutarse para todas las decisiones.

Debe utilizarse cuando la acción afecte a:

- código;
- configuración;
- scripts;
- servicios;
- automatización;
- seguridad;
- repo hygiene.

Debe omitirse en:

- consultas documentales;
- búsquedas simples;
- documentación aislada;
- lectura informativa.

## Cuándo usar TASK_VALIDATOR

`TASK_VALIDATOR` es la puerta final antes de permitir una acción.

Debe recibir:

```text
request
action_class
risk_level
context_budget
dependency_result (si aplica)
```

Resultados permitidos:

```text
ALLOW
REVIEW
BLOCK
```

## Regla de no recursión

Por decisión:

```text
DEPENDENCY_CHECKER
máximo una ejecución
```

```text
TASK_VALIDATOR
máximo una ejecución
```

Flujo válido:

```text
DEPENDENCY_CHECKER
        ↓
TASK_VALIDATOR
```

Flujo no válido:

```text
TASK_VALIDATOR
        ↓
DEPENDENCY_CHECKER
        ↓
TASK_VALIDATOR
```

## Runner

El runner nunca debe actuar por iniciativa propia.

Solo puede ejecutarse cuando:

```text
TASK_VALIDATOR = ALLOW
```

Debe permanecer bloqueado cuando el resultado sea:

```text
REVIEW
BLOCK
```

## Flujo operativo resumido

```text
REQUEST
      ↓
MODEL CHECK
      ↓
CONTEXT BUDGET
      ↓
SUMMARY CHECK
      ↓
DEPENDENCY_CHECKER (si aplica)
      ↓
TASK_VALIDATOR
      ↓
ALLOW / REVIEW / BLOCK
      ↓
RUNNER (solo ALLOW)
```

## Decision Trace

Toda decisión debe producir una traza visible y compacta.

La traza existe para responder:

- qué se decidió;
- qué contexto se utilizó;
- quién validó;
- por qué se permitió o bloqueó.

No debe contener razonamiento largo.

## Formato recomendado

```text
DECISION_TRACE:
- request_id: <id>
- action_class: DOCS/CODE/CONFIG/SERVICE/SECURITY
- risk_level: LOW/MEDIUM/HIGH/CRITICAL
- model_required: YES/NO
- context_budget: LOW/MEDIUM/HIGH/CRITICAL
- summary_used: YES/NO
- source_doc_loaded: YES/NO
- summary_status: FRESH/STALE/DEPRECATED/NA
- dependency_check: SKIPPED/D0/D1/D2/D3
- dependency_result: PASS/REVIEW/BLOCK/NA
- task_validator_result: ALLOW/REVIEW/BLOCK
- runner_allowed: YES/NO
- decision_cost: LOW/MEDIUM/HIGH/CRITICAL
- result: ALLOW/REVIEW/BLOCK
- reason: <compact reason>
```

## Auditoría visible

Una decisión debe permitir verificar:

- por qué se permitió;
- por qué se bloqueó;
- qué contexto se cargó;
- si se utilizó summary;
- si se cargó source_doc;
- si intervino DEPENDENCY_CHECKER;
- si el runner estaba autorizado.

## Reglas de detalle

Para decisiones:

```text
LOW
MEDIUM
```

la traza debe permanecer compacta.

Para decisiones:

```text
HIGH
CRITICAL
```

debe incluir una razón operativa breve.

## Qué no debe almacenarse

```text
chain of thought
logs completos
documentos completos
secretos
tokens
```

## Riesgos

### Riesgo 1

Flujo demasiado complejo.

Mitigación:

```text
mantener flujo mínimo
```

### Riesgo 2

Trazas demasiado grandes.

Mitigación:

```text
telemetría compacta
```

### Riesgo 3

Summaries obsoletos.

Mitigación:

```text
summary_status = STALE
```

### Riesgo 4

Escalado excesivo de contexto.

Mitigación:

```text
summary first
source on demand
```

## Decisión estratégica

Neodaemon debe ser:

```text
auditable
predecible
eficiente
```

Toda decisión debe poder explicarse mediante una `DECISION_TRACE`.

## Próximo paso recomendado

Definir especificaciones operativas v0.1 para:

- TASK_VALIDATOR;
- DEPENDENCY_CHECKER;
- DECISION_TRACE.

No avanzar hacia automatización avanzada hasta disponer de trazabilidad mínima verificable.


