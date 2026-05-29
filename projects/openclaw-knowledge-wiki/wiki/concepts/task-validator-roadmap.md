# TASK_VALIDATOR roadmap

## Estado

Roadmap creado.

## Propósito

`TASK_VALIDATOR` debe convertirse en el primer componente formal del razonador operativo de Neodaemon.

Su función no es ejecutar acciones.

Su función es decidir si una acción propuesta puede avanzar hacia ejecución, debe bloquearse o requiere más contexto.

## Problema que resuelve

Neodaemon necesita evitar que una acción parezca segura solo porque:

- está bien redactada;
- contiene keywords correctas;
- parece low-risk;
- afecta a documentación;
- no modifica código directamente.

La experiencia reciente mostró que acciones aparentemente simples pueden esconder dependencias activas, rutas absolutas, tokens hardcodeados o impacto operativo.

## Principio central

`TASK_VALIDATOR` debe funcionar como router de riesgo, no como lector masivo de contexto.

Acción simple → validación simple.

Acción sensible → validación profunda.

Acción desconocida → BLOCK.

## Alcance

`TASK_VALIDATOR` aplica antes de:

- crear documentación;
- modificar documentación;
- crear código;
- modificar código;
- tocar runners;
- tocar policies;
- tocar tests;
- mover archivos;
- borrar archivos;
- tocar servicios;
- tocar configuración;
- ejecutar Git automation.

## Fuera de alcance

`TASK_VALIDATOR` no debe:

- ejecutar acciones;
- modificar archivos;
- hacer commit;
- hacer push;
- crear PR;
- hacer merge;
- tocar secretos;
- tocar `.env`;
- tocar gateway;
- tocar OAuth;
- tocar systemd;
- saltarse autorización humana.

## Inputs obligatorios

Toda validación debe recibir como mínimo:

- `action_requested`;
- `target_paths`;
- `scope`;
- `expected_changes`;
- `affected_components`;
- `forbidden_paths`;
- `rollback_plan`;
- `validation_plan`;
- `safe_to_execute`;
- `operator_authorization`.

Si faltan inputs obligatorios, el resultado debe ser `BLOCK`.

## Formato obligatorio de salida

```text
TASK_VALIDATOR:
- action_classification: DOCS_ONLY/CODE/CONFIG/SERVICE/SECURITY/GIT_AUTOMATION/UNKNOWN
- scope: LOW/MEDIUM/HIGH/CRITICAL
- context_level: L0/L1/L2/L3
- affected_paths: OK/ERROR
- forbidden_paths_check: OK/ERROR
- dependency_check: OK/ERROR/NOT_APPLICABLE
- rollback_plan: OK/ERROR/NOT_APPLICABLE
- validation_plan: OK/ERROR
- evidence_quality: OK/ERROR
- uncertainty_level: LOW/MEDIUM/HIGH
- safe_to_execute: OK/ERROR
- result: PASS/BLOCK
```

## Niveles de riesgo

### LOW

Acciones documentales simples.

Ejemplos:

- crear nota conceptual;
- actualizar index/log;
- no tocar código;
- no tocar servicios;
- no tocar configuración.

### MEDIUM

Acciones que afectan a tests, runners no ejecutados o documentación técnica con impacto futuro.

Ejemplos:

- modificar tests;
- modificar policy documental;
- preparar plan de runner;
- modificar documentación que habilita automatización futura.

### HIGH

Acciones con posible impacto operativo.

Ejemplos:

- modificar Python activo;
- modificar scripts usados por servicios;
- mover archivos raíz;
- tocar rutas absolutas;
- tocar automatizaciones.

### CRITICAL

Acciones sobre componentes sensibles.

Ejemplos:

- tokens;
- `.env`;
- OAuth;
- gateway;
- systemd;
- auth;
- logs crudos;
- secretos;
- merge automático;
- borrado irreversible.

## Estrategia de consumo de tokens

`TASK_VALIDATOR` no debe cargar todo el contexto del proyecto por defecto.

Debe usar el contexto mínimo suficiente para decidir.

El consumo esperado debe escalar según riesgo:

- L0: clasificación rápida, contexto mínimo.
- L1: validación low-risk, documentos relevantes.
- L2: validación medium-risk, reglas y artefactos relacionados.
- L3: validación high-risk o critical, dependencias, servicios, historial y rollback.

## Presupuesto orientativo de tokens

### L0 — Clasificación rápida

Uso aproximado:

- 500 tokens.

Objetivo:

- clasificar acción;
- detectar si parece low-risk, medium-risk, high-risk o critical.

### L1 — Validación low-risk

Uso aproximado:

- 500 a 1.500 tokens.

Usar solo:

- solicitud;
- archivos objetivo;
- regla aplicable;
- index/log si aplica.

### L2 — Validación medium-risk

Uso aproximado:

- 1.500 a 4.000 tokens.

Usar:

- solicitud;
- regla aplicable;
- runner/policy/test relacionado;
- documentación conectada;
- riesgos conocidos.

### L3 — Validación high-risk/critical

Uso aproximado:

- 4.000 a 10.000+ tokens.

Usar:

- mapas de dependencias;
- systemd si aplica;
- scripts relacionados;
- imports;
- rutas absolutas;
- historial de decisiones;
- rollback;
- validaciones previas.

## Regla de bloqueo por contexto insuficiente

Si `TASK_VALIDATOR` no tiene contexto suficiente para validar una acción, debe devolver `BLOCK`.

No debe inventar seguridad.

No debe asumir que una acción es segura por ausencia de evidencia.

## Evidencia y certeza

Toda validación debe distinguir entre:

- hecho verificado;
- evidencia parcial;
- inferencia razonable;
- hipótesis;
- desconocido.

Si una decisión depende de hipótesis no verificadas, el resultado debe ser `BLOCK` o requerir más contexto.

## Relación con DESIGN_DOC_CHECK

`DESIGN_DOC_CHECK` valida calidad documental y coherencia conceptual.

`TASK_VALIDATOR` decide si la acción asociada puede avanzar hacia ejecución.

Un documento puede pasar `DESIGN_DOC_CHECK` y aun así quedar bloqueado por `TASK_VALIDATOR` si afecta a rutas, servicios o dependencias no verificadas.

## Relación con SELF_CHECK_PYTHON

`SELF_CHECK_PYTHON` aplica a propuestas o cambios Python.

`TASK_VALIDATOR` debe invocarlo cuando la acción implique:

- crear Python;
- modificar Python;
- ejecutar Python;
- validar runner Python;
- modificar tests Python.

Si `SELF_CHECK_PYTHON` falta en una acción Python, `TASK_VALIDATOR` debe bloquear.

## Relación con DEPENDENCY_CHECKER

`DEPENDENCY_CHECKER` debe informar sobre:

- rutas absolutas;
- imports;
- systemd;
- scripts;
- servicios;
- referencias cruzadas;
- dependencias activas.

Si una acción toca archivos con dependencias desconocidas, `TASK_VALIDATOR` debe bloquear.

## Relación con GitHub runner

El runner GitHub no debe ejecutar acciones sin pasar por `TASK_VALIDATOR`.

En v0.1, el runner solo soporta `plan` y `check`.

En v0.2, cualquier `copy` controlado debe requerir:

- clasificación de riesgo;
- validación de paths;
- validación de rollback;
- validación de run_state;
- bloqueo de symlinks;
- bloqueo path traversal;
- evidencia suficiente.

## Roadmap de implementación

### v0.1 — Checklist documental

- definir formato;
- aplicar manualmente;
- usar en propuestas sensibles.

### v0.2 — Formato obligatorio

- convertir salida en bloque estructurado;
- exigir inputs obligatorios;
- aplicar en workflows documentales.

### v0.3 — Checker semiautomático

- validar presencia de campos;
- detectar rutas prohibidas;
- detectar contradicciones simples;
- detectar falta de rollback.

### v1.0 — Integración con runner

- bloquear acciones del runner si falla;
- registrar decisión;
- registrar evidencia;
- registrar nivel de contexto usado;
- registrar `safe_to_execute`.

## Tests futuros

Deben existir tests para:

- acción documental low-risk;
- acción Python sin `SELF_CHECK_PYTHON`;
- acción con ruta prohibida;
- acción sobre systemd;
- acción con rollback ausente;
- acción con contexto insuficiente;
- acción con `safe_to_execute` contradictorio;
- acción Git automation sin autorización;
- acción con dependencia desconocida.

## Criterios de bloqueo

`TASK_VALIDATOR` debe devolver `BLOCK` si:

- faltan inputs obligatorios;
- hay rutas prohibidas;
- hay dependencias desconocidas;
- falta rollback cuando aplica;
- falta validación posterior;
- `safe_to_execute` contradice la acción;
- se toca componente sensible sin autorización;
- se propone automatización Git no permitida;
- se confunden hipótesis con hechos;
- se intenta ejecutar sin evidencia suficiente.

## Riesgos

### Riesgo 1 — Exceso de tokens

Mitigación:

- usar niveles L0 a L3;
- cargar contexto mínimo;
- escalar solo por riesgo.

### Riesgo 2 — Falsa seguridad

Mitigación:

- bloquear si falta evidencia;
- distinguir hechos de hipótesis.

### Riesgo 3 — Convertirse en burocracia

Mitigación:

- low-risk debe ser ligero;
- high-risk debe ser profundo.

### Riesgo 4 — Aprobar por keywords

Mitigación:

- validar contenido operativo;
- no aceptar campos vacíos o superficiales.

## Próximo paso recomendado

Antes de implementar código, usar este roadmap como base para una especificación `TASK_VALIDATOR` v0.1.

La primera implementación debe ser conservadora, documental y bloqueante por defecto.

No debe ejecutar acciones.


