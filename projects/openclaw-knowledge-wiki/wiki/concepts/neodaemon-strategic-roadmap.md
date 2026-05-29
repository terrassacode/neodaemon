# Neodaemon strategic roadmap

## Estado

Roadmap estratégico creado.

## Propósito

Este documento consolida la dirección estratégica de Neodaemon después de los PRs #21 a #27.

La conclusión principal es que el objetivo del proyecto no es simplemente automatizar GitHub.

La automatización GitHub es un caso de uso.

El objetivo principal es construir un operador confiable capaz de comprender contexto, evaluar riesgo, justificar decisiones, recordar decisiones anteriores y automatizar únicamente acciones seguras.

## Principio central

Antes de crear un agente que haga cosas, hay que crear un agente que sepa por qué las hace.

## Contexto documentado

Entre los PRs #21 y #27 se incorporaron piezas clave:

- PR #21: `github_pr_workflow_runner.py` v0.1, solo `plan` y `check`.
- PR #22: `SELF_CHECK_PYTHON`.
- PR #23: tests del runner v0.1.
- PR #24: diseño v0.2 para `copy` controlado.
- PR #25: `DESIGN_DOC_CHECK`.
- PR #26: mapa de inventario y riesgos de la raíz del repositorio.
- PR #27: revisión de seguridad de backups API y tokens hardcodeados.

Estas piezas indican una transición desde scripts dispersos hacia un sistema gobernado.

## Revisión estratégica

La hipótesis inicial era que el proyecto avanzaba hacia automatización GitHub.

La revisión actual corrige esa hipótesis:

- GitHub no es el producto principal.
- GitHub es un dominio de prueba.
- El producto real es el razonador operativo de Neodaemon.

## Fase 0 — Observabilidad

Objetivo: entender antes de actuar.

Debe incluir:

- inventario de componentes;
- mapa de servicios;
- mapa de rutas absolutas;
- mapa de dependencias;
- mapa de scripts activos;
- mapa de secretos;
- mapa de automatizaciones;
- estado real de systemd;
- estado real de Telegram/RAG/Gateway.

Motivo:

No se puede gobernar con seguridad aquello que no se entiende.

Estado:

- Iniciada mediante los PRs #26 y #27.

## Fase 1 — Gobernanza

Objetivo: impedir acciones peligrosas antes de automatizar.

Componentes:

- `SELF_CHECK_PYTHON`;
- `DESIGN_DOC_CHECK`;
- políticas de ejecución;
- criterios de bloqueo;
- validación de estado frente a acción;
- revisión de alcance;
- revisión de rutas sensibles.

Estado:

- Parcialmente implementada.

## Fase 2 — Memoria de decisiones

Objetivo: evitar que Neodaemon repita errores o contradiga decisiones previas.

Debe permitir:

- recuperar decisiones anteriores;
- comparar una propuesta nueva contra decisiones previas;
- detectar contradicciones históricas;
- registrar motivos, no solo resultados;
- distinguir decisiones firmes de hipótesis.

Estado:

- Pendiente.

## Fase 3 — Motor de razonamiento operativo

Objetivo: evaluar qué debe hacerse antes de decidir cómo hacerlo.

Debe responder:

- qué se quiere hacer;
- por qué se quiere hacer;
- qué evidencia existe;
- qué dependencias hay;
- qué riesgos existen;
- qué alternativas hay;
- qué bloquea la acción;
- qué rollback existe;
- qué validación posterior aplica.

Componentes futuros:

- `TASK_VALIDATOR`;
- `DEPENDENCY_CHECKER`;
- `CONTRADICTION_CHECKER`;
- `RISK_SCORER`;
- `STATE_ACTION_CONSISTENCY`;
- `EXPLAINABILITY_ENGINE`.

Estado:

- Conceptual.
- Parcialmente ejercitado manualmente durante PRs #25, #26 y #27.

## Fase 4 — Automatización GitHub segura

Objetivo: automatizar solo acciones GitHub controladas, reversibles y auditables.

Estado actual:

- runner v0.1 implementado;
- solo soporta `plan` y `check`;
- no ejecuta `copy`;
- no ejecuta commit;
- no ejecuta push;
- no crea PR;
- no hace merge.

Siguiente paso técnico:

- implementar v0.2 `copy` controlado;
- añadir tests v0.2;
- validar snapshot;
- validar rollback;
- validar bloqueo de symlinks;
- validar bloqueo de path traversal;
- mantener `run_state` fuera de Git.

Condición:

No avanzar a commit, push, PR o merge hasta que `copy` sea seguro y testado.

## Fase 5 — Profesionalización del repositorio

Objetivo: mejorar estructura sin romper producción.

Estado actual:

- la raíz contiene archivos sueltos;
- algunos parecen históricos;
- algunos contienen tokens hardcodeados;
- varios archivos raíz están acoplados a rutas absolutas;
- systemd y scripts operativos dependen de rutas actuales.

Regla:

No mover archivos raíz activos sin trazado completo de dependencias.

Antes de reorganizar:

- inventariar;
- clasificar;
- detectar imports;
- revisar systemd;
- revisar scripts;
- crear wrappers si hace falta;
- validar servicios;
- validar Telegram;
- validar RAG.

## Fase 6 — Trusted Operator

Objetivo final: Neodaemon debe convertirse en un operador confiable.

No significa autonomía total.

Significa:

- comportamiento predecible;
- razonamiento explícito;
- decisiones auditables;
- memoria de contexto;
- bloqueo de acciones peligrosas;
- automatización limitada;
- trazabilidad;
- rollback;
- explicabilidad.

## Principios estratégicos

1. Seguridad antes que productividad.
2. Comprender antes de actuar.
3. Justificar antes de automatizar.
4. Recordar antes de decidir.
5. Bloquear si falta evidencia.
6. No confundir documentación con implementación.
7. No confundir GitHub automation con razonamiento operativo.
8. No mover estructura si hay dependencias activas.
9. No borrar secretos sin rotación.
10. No afirmar validación si solo se revisaron keywords.

## Riesgos del roadmap

### Riesgo 1: documentar demasiado

Crear documentos sin convertirlos en comportamiento real puede generar falsa sensación de avance.

Mitigación:

Cada documento estratégico debe acabar derivando en validaciones, tests o reglas ejecutables.

### Riesgo 2: automatizar Git demasiado pronto

Automatizar commit, push, PR o merge antes de tener razonamiento operativo puede romper el repositorio.

Mitigación:

Mantener v0.1/v0.2 dentro de límites estrictos.

### Riesgo 3: limpiar el repo antes de desacoplar rutas

Mover archivos por estética puede romper servicios.

Mitigación:

Completar trazado de dependencias antes de cualquier reestructura.

### Riesgo 4: confundir hipótesis con hechos

Neodaemon debe distinguir entre evidencia verificada, inferencia razonable e hipótesis.

Mitigación:

Añadir clasificación explícita de certeza en futuras validaciones.

## Decisión estratégica

La prioridad no debe ser automatizar más rápido.

La prioridad debe ser mejorar la capacidad de Neodaemon para razonar, justificar y bloquear.

GitHub automation continuará siendo un banco de pruebas controlado para desarrollar ese razonador.

## Próximo paso recomendado

Antes de implementar nuevas acciones Git, convertir este roadmap en referencia de proyecto.

Después, avanzar hacia:

1. `TASK_VALIDATOR` formal.
2. `DEPENDENCY_CHECKER`.
3. implementación controlada de runner v0.2 `copy`.
4. tests v0.2.
5. revisión posterior antes de cualquier commit/push/PR automation.



