# DESIGN_DOC_CHECK — regla obligatoria de revisión documental

## Estado

Regla creada.

## Propósito

`DESIGN_DOC_CHECK` es una regla obligatoria para revisar documentos técnicos de diseño antes de crearlos, versionarlos o usarlos como base para automatización futura.

Su objetivo es evitar falsos OK basados solo en keywords, títulos o estructura superficial.

Keywords no son suficiente.

## Cuándo aplica

Debe aplicarse antes de crear o versionar documentos como:

- planes de runner;
- planes de automation;
- cambios de policy;
- diseños de rollback;
- diseños de secret scan;
- diseños de Git/GitHub automation;
- cualquier documento que pueda influir en ejecución futura.

## Checklist obligatoria

Toda revisión `DESIGN_DOC_CHECK` debe evaluar:

- required_sections;
- required_points;
- evidence_quality;
- contradictions;
- scope_limits;
- security_boundaries;
- risk_section;
- block_criteria;
- rollback_recovery;
- testability;
- decision_traceability;
- state_action_consistency;
- no_hidden_execution;
- implementation_claims;
- safe_to_execute;
- result.

## Formato obligatorio de salida

```text
DESIGN_DOC_CHECK:
- required_sections: OK/ERROR
- required_points: OK/ERROR
- evidence_quality: OK/ERROR
- contradictions: OK/ERROR
- scope_limits: OK/ERROR
- security_boundaries: OK/ERROR
- risk_section: OK/ERROR
- block_criteria: OK/ERROR
- rollback_recovery: OK/ERROR/NOT_APPLICABLE
- testability: OK/ERROR
- decision_traceability: OK/ERROR
- state_action_consistency: OK/ERROR
- no_hidden_execution: OK/ERROR
- implementation_claims: OK/ERROR
- safe_to_execute: OK/ERROR
- result: PASS/BLOCK

## Criterios de bloqueo

La revisión debe devolver `result: BLOCK` si ocurre cualquiera de estos casos:

- falta una sección obligatoria;
- falta un punto obligatorio;
- hay contradicciones internas;
- solo hay keywords sin explicación operativa;
- el documento afirma implementación real cuando solo describe diseño;
- el documento contiene ejecución encubierta;
- el documento propone acciones no autorizadas;
- el estado declarado contradice las acciones propuestas;
- no existe forma razonable de validar el resultado.

## Prohibiciones explícitas

No está prohibido usar términos como aprobado, validado, implementado, seguro o sin riesgo.

Sí está prohibido usarlos cuando:

- no exista evidencia real suficiente;
- solo se hayan validado keywords;
- solo se haya validado estructura superficial;
- el uso del término cree una falsa sensación de ejecución o seguridad.

## Contradicciones

Una contradicción debe bloquear la revisión.

Ejemplos:

- declarar `safe_to_execute=false` y proponer escritura real;
- decir diseño únicamente y afirmar implementado;
- declarar rollback obligatorio y no explicar cómo se recupera;
- registrar como creado algo que no existe o no fue verificado.

## Implementación encubierta

Hay implementación encubierta si un documento, bajo apariencia de diseño o documentación, incluye pasos que ejecutan cambios reales sin autorización explícita.

Ejemplos:

- modificar runner, policy o tests fuera del alcance aprobado;
- ejecutar Git cuando la revisión era documental;
- hacer commit, push, PR o merge sin autorización;
- tocar raw/, gateway, auth, tokens, systemd, .env o logs crudos sin permiso explícito.

## Rollback y recovery

Si el documento propone cambios que puedan modificar archivos, estado local o automatización futura, debe explicar rollback/recovery.

Debe indicar:

- cuándo aplica;
- qué se restaura;
- desde dónde se restaura;
- cómo se valida la recuperación;
- qué bloquea si la recuperación no puede garantizarse.

Si rollback no aplica, debe justificarse como `NOT_APPLICABLE`.

## Testabilidad

Un documento válido debe explicar cómo se comprobará su resultado.

La testabilidad puede incluir:

- existencia de archivos;
- presencia de entradas en índice;
- presencia de entradas append-only en log;
- grep de términos obligatorios;
- comparación de paths tocados;
- verificación de que no se modificaron rutas prohibidas.

## Coherencia entre estado y acción

El estado declarado debe coincidir con la acción real.

Ejemplos:

- Si el log dice regla creada, el archivo debe existir.
- Si el documento dice propuesta, el log no debe marcarla como creada.
- Si se declara `safe_to_execute=false`, no debe haber ejecución.
- Si se declara Regla creada, debe existir evidencia local o en repo.

## Aplicación específica a runner y automation

En planes de runner o automation, `DESIGN_DOC_CHECK` debe exigir revisión explícita de:

- comandos implementados y no implementados;
- safe_to_execute;
- path traversal;
- symlink protection;
- snapshot;
- rollback;
- secret scan;
- run_state fuera de Git;
- no `git add .`;
- no auto merge;
- no commit/push/PR/merge sin autorización;
- no claims de implementación si solo existe diseño.

## Límites de esta regla

Esta regla:

- no ejecuta Git;
- no crea código;
- no modifica runner;
- no modifica policy;
- no sustituye tests;
- no sustituye revisión humana;
- no convierte una propuesta en implementación;
- no autoriza acciones futuras por sí misma.
