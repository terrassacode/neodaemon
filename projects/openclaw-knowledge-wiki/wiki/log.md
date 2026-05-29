# OpenClaw Knowledge Wiki — Log

Registro append-only de ingests y cambios relevantes.

## Reglas

- No reescribir entradas anteriores.
- Añadir nuevas entradas al final.
- Registrar máximo 3 fuentes por ingest.
- Separar fuentes, notas generadas y límites.
- No modificar `raw/`.
- No registrar automatizaciones no ejecutadas.

---

## Entradas

### 2026-05-27 — Primer ingest manual ejecutado

## Fuentes

- `raw/notes/first-source-openclaw-knowledge-wiki-readme.md`

## Notas generadas

- `wiki/sources/first-source-openclaw-knowledge-wiki-readme.md`

## Tipo

Ingest manual de prueba.

## Límites

- Una única fuente.
- Fuente interna no sensible.
- Sin APIs externas.
- Sin scripts globales.
- Sin dependencias.
- Sin modificar `raw/` después de la copia inicial.
- Sin escribir fuera del proyecto.

## Resultado esperado

Validar si el flujo `raw/` → `wiki/` → `index/log` es claro, trazable y razonable para operación real.

### 2026-05-27 — Lint manual del primer ingest validado

## Revisión

Se revisó el primer ingest manual basado en:

- `raw/notes/first-source-openclaw-knowledge-wiki-readme.md`
- `wiki/sources/first-source-openclaw-knowledge-wiki-readme.md`
- `wiki/index.md`
- `wiki/log.md`

## Resultado

El flujo mínimo `raw/` → `wiki/` → `index/log` → lint manual queda validado.

## Observaciones

- La nota tiene fuente clara.
- Distingue datos confirmados, inferencias y dudas.
- No se detectaron secretos.
- No se detectaron claims problemáticos.
- No se detectó escritura fuera del proyecto.
- No se recomienda modificar el log anterior.

## Estado

Primer ingest y lint manual: OK.

### 2026-05-27 — Segundo ingest manual ejecutado

## Fuentes

- `raw/docs/project-isolation-policy.md`

## Notas generadas

- `wiki/sources/project-isolation-policy.md`

## Tipo

Ingest manual de política operativa interna.

## Límites

- Una única fuente.
- Fuente interna no sensible.
- Sin APIs externas.
- Sin scripts globales.
- Sin dependencias.
- Sin modificar `raw/` después de la copia inicial.
- Sin escribir fuera del proyecto salvo lectura autorizada de la fuente original.
- Sin tocar core, scripts globales, dashboard-v2, logs, memory, RAG, Gmail, Telegram, systemd ni gateway.

## Resultado esperado

Incorporar a la wiki conocimiento trazable sobre la política de aislamiento de proyectos para futuras consultas y validaciones manuales.

### 2026-05-27 — Lint manual del segundo ingest validado

## Revisión

Se revisó el segundo ingest manual basado en:

- `raw/docs/project-isolation-policy.md`
- `wiki/sources/project-isolation-policy.md`
- `wiki/index.md`
- `wiki/log.md`

## Resultado

El segundo ingest queda validado como correcto y conservador.

## Observaciones

- La nota tiene fuente clara.
- Distingue datos confirmados, inferencias y dudas.
- No se detectaron secretos.
- No se detectaron claims sin fuente.
- No suaviza restricciones de seguridad.
- No contradice `PROJECT_ISOLATION_POLICY.md`.
- No se detectó escritura fuera del proyecto.
- No se recomienda modificar el log anterior.

## Estado

Segundo ingest y lint manual: OK.

### 2026-05-27 — Nota conceptual project-core-boundary creada

## Fuentes wiki usadas

- `wiki/sources/project-isolation-policy.md`
- `wiki/sources/first-source-openclaw-knowledge-wiki-readme.md`
- `NEODAEMON_WIKI.md`
- `wiki/index.md`

## Nota creada

- `wiki/concepts/project-core-boundary.md`

## Tipo

Nota conceptual derivada.

## Límites

- No se leyó `raw/`.
- No se creó fuente nueva.
- Sin APIs externas.
- Sin scripts globales.
- Sin dependencias.
- Sin escribir fuera del proyecto.
- Sin suavizar restricciones de seguridad.

## Resultado esperado

Crear una guía operacional breve sobre cómo distinguir proyecto y core, manteniendo trazabilidad hacia las notas fuente existentes.

### 2026-05-27 — Lint manual de nota conceptual project-core-boundary

## Archivo revisado

- `wiki/concepts/project-core-boundary.md`

## Tipo

Lint manual de nota conceptual.

## Resultado

PASS.

## Warnings

- La checklist omite `briefings`, `backups` y `git_clean`, aunque sí aparecen antes en “Datos confirmados”.
- “zona segura” es una inferencia razonable, pero debe entenderse como segura solo bajo restricciones de aislamiento.

## Decisión

No modificar ahora.

### 2026-05-27 — Lint manual de project-core-boundary validado

## Revisión

Se revisó la nota conceptual:

- `wiki/concepts/project-core-boundary.md`

## Resultado

La nota queda validada como correcta y usable.

## Observaciones

- Tiene fuentes claras.
- No cita archivos inexistentes.
- Distingue datos confirmados, inferencias y dudas.
- No suaviza restricciones de seguridad.
- No convierte la checklist en autorización automática.
- Mantiene que las dudas requieren autorización explícita de Albert.
- No contradice project-isolation-policy.
- No requiere leer raw/.
- No se detectaron secretos.
- No se detectaron claims sin fuente.

## Estado

Nota conceptual project-core-boundary: OK.

### 2026-05-28 — Obsidian conectado como vault local

## Tipo

Hito operativo local.

## Descripción

Obsidian queda conectado como vault local para visualizar y editar Markdown dentro del proyecto OpenClaw Knowledge Wiki.

## Límites

- Obsidian es opcional.
- No es dependencia obligatoria.
- No razona, no ingiere fuentes y no valida contenido.
- No introduce automatización.
- No usa APIs externas.
- No modifica `raw/` por sí mismo.
- La generación y mantenimiento de la wiki sigue correspondiendo a Neodaemon bajo autorización de Albert.

## Estado

Obsidian vault local: OK.

### 2026-05-28 — Nota conceptual obsidian-operating-rules creada

## Fuentes wiki usadas

- `README.md`
- `NEODAEMON_WIKI.md`
- `wiki/log.md`
- `wiki/concepts/project-core-boundary.md`

## Nota creada

- `wiki/concepts/obsidian-operating-rules.md`

## Tipo

Nota conceptual operativa.

## Límites

- No se leyó `raw/`.
- No se creó fuente nueva.
- Sin APIs externas.
- Sin scripts globales.
- Sin dependencias.
- Sin instalar plugins.
- Sin Obsidian Sync.
- Sin tocar gateway, auth ni tokens.
- Sin escribir fuera del proyecto.

## Resultado esperado

Definir reglas claras para usar Obsidian como visor/editor Markdown local sin romper aislamiento, trazabilidad ni seguridad.

### 2026-05-28 — github-pr-workflow-skill-design creada

## Fuentes wiki usadas

- `wiki/concepts/project-core-boundary.md`
- `wiki/concepts/obsidian-operating-rules.md`
- reglas operativas confirmadas por Albert para el diseño GitHub PR workflow skill

## Nota creada

- `wiki/concepts/github-pr-workflow-skill-design.md`

## Tipo

Nota conceptual de diseño operativo.

## Límites

- No se leyó `raw/`.
- No se creó skill real.
- Sin ejecutar Git.
- Sin tocar `~/.openclaw/skills`.
- Sin tocar gateway, auth ni tokens.
- Sin tocar systemd.
- Sin tocar `.env`.
- Sin leer logs crudos.
- Sin escribir fuera del proyecto.

## Resultado esperado

Documentar un MVP seguro para asistir flujos GitHub PR manuales sin autopilot, con allowlist, bloqueo por defecto, secret scan silencioso, separación de fases y merge automático prohibido.

### 2026-05-28 — github-pr-workflow-skill dry-run v2 documentado

## Skill evaluada

- `skills/github-pr-workflow/SKILL.md`

## Nota creada

- `wiki/concepts/github-pr-workflow-skill-dry-run-v2.md`

## Tipo

Registro conceptual de dry-run.

## Resultado

APROBADO.

## Validación conceptual

La simulación confirmó que la skill distingue correctamente:

- workspace source;
- repo target;
- rutas Git relativas.

## Límites

- No se ejecutó Git.
- No se creó rama.
- No se copiaron archivos.
- No se hizo secret scan real.
- No hubo commit.
- No hubo push.
- No hubo PR.
- No hubo merge.
- No se instaló la skill.
- No se tocó `~/.openclaw/skills`.
- No se tocaron gateway, auth, tokens, systemd, `.env` ni logs crudos.
- No se tocó `raw/`.

## Estado

Dry-run conceptual v2: OK.

### 2026-05-28 — github-pr-workflow-skill first real minimal test Fase 1 creada

## Skill usada

- `skills/github-pr-workflow/SKILL.md`

## Nota creada

- `wiki/concepts/github-pr-workflow-skill-first-real-test.md`

## Tipo

Registro de primera prueba real mínima, limitada a workspace.

## Límites

- Solo Fase 1 workspace.
- Sin ejecutar Git.
- Sin crear rama.
- Sin copiar al repo limpio.
- Sin secret scan real.
- Sin commit.
- Sin push.
- Sin PR.
- Sin merge.
- Sin modificar la skill.
- Sin tocar `~/.openclaw/skills`.
- Sin tocar gateway, auth, tokens, systemd, `.env` ni logs crudos.
- Sin tocar `raw/`.
- Sin escribir fuera del proyecto.

## Resultado

Fase 1 creada y validada en workspace.

### 2026-05-28 — github-pr-workflow-runner-design creada

## Nota creada

- `wiki/concepts/github-pr-workflow-runner-design.md`

## Tipo

Diseño técnico corregido para runner de automatización controlada.

## Alcance

Diseño de `github_pr_workflow_runner.py` para evolución gradual hacia automatización completa de `DOCS_LOW_RISK`.

## Límites

- No se creó runner real.
- No se creó policy real.
- No se creó `.gitignore`.
- No se creó `run_state`.
- Sin ejecutar Git.
- Sin instalar dependencias.
- Sin tocar `~/.openclaw/skills`.
- Sin tocar gateway, auth, tokens, systemd, `.env` ni logs crudos.
- Sin tocar `raw/`.
- Sin escribir fuera del proyecto.

## Correcciones incorporadas

- Ruta `automation/github_pr_workflow_runner.py`, no `tools/`.
- Policy en `automation/policies/github_pr_workflow.policy.yml`.
- `automation/run_state/` no versionado por defecto.
- v0.1 solo `plan/check`.
- Sin comando `merge` en v0.1.
- Approval mediante `--approval-file` o `--confirm-risk`, no tokens secretos.
- Checks de symlink, realpath y path traversal.
- Snapshot antes de copiar.
- Branch existente bloquea salvo recovery explícito.
- Revalidación post-copy.
- Bloqueo de binarios, encoding no UTF-8 y tamaños excesivos.
- Aclarado que patrones `**/*token*` bloquean nombres de archivo; contenido tipo `token=` va por secret scan silencioso.
- Aclarado que `allow_auto_commit`, `allow_auto_push` y `allow_auto_pr` son objetivo de madurez, no comportamiento activo en v0.1.

## Estado

Diseño técnico corregido: creado.

### 2026-05-28 — python-code-self-check-rule creada

## Nota creada

- `wiki/concepts/python-code-self-check-rule.md`

## Tipo

Regla operativa para propuestas y cambios Python.

## Contenido

Documenta `SELF_CHECK_PYTHON` como revisión obligatoria antes de proponer o crear código Python.

## Límites

- No se creó código Python.
- No se ejecutaron tests.
- Sin ejecutar Git.
- Sin tocar runner.
- Sin tocar policy.
- Sin tocar `raw/`.
- Sin tocar `~/.openclaw/skills`.
- Sin tocar gateway, auth, tokens, systemd, `.env` ni logs crudos.
- Sin escribir fuera del proyecto.

## Estado

Regla creada.

### 2026-05-28 — github-pr-workflow-runner-v0-2-copy-plan creada

## Nota creada

- `wiki/concepts/github-pr-workflow-runner-v0-2-copy-plan.md`

## Tipo

Plan técnico previo a implementación.

## Contenido

Documenta criterios obligatorios para implementar `copy` automático controlado en `github_pr_workflow_runner.py` v0.2, incluyendo snapshot, copy atómico, hash source before/after, permisos no ejecutables, validación de tamaño antes de leer contenido completo, revalidación, symlink/path traversal checks, bloqueo de rutas prohibidas y rollback sin `git reset --hard`.

## Límites

- No se creó código Python.
- No se modificó runner.
- No se modificó policy.
- No se creó `run_state`.
- No se copiaron archivos reales.
- Sin ejecutar Git.
- Sin tocar repo limpio.
- Sin commit, push, PR ni merge.
- Sin tocar `raw/`.
- Sin tocar `~/.openclaw/skills`.
- Sin tocar gateway, auth, tokens, systemd, `.env` ni logs crudos.
- Sin escribir fuera del proyecto.

## Estado

Plan creado.

### 2026-05-29 — design-doc-check-rule creada

## Tipo

Regla documental obligatoria.

## Nota creada

- `wiki/concepts/design-doc-check-rule.md`

## Límites

- No se creó código Python.
- No se modificó runner.
- No se modificó policy.
- No se ejecutó Git como parte de la regla.
- No se tocó `raw/`.
- No se tocó gateway, auth, tokens, systemd, `.env` ni logs crudos.

## Resultado esperado

Establecer `DESIGN_DOC_CHECK` como regla obligatoria para revisar calidad documental, evidencia, contradicciones, límites, criterios de bloqueo, rollback/recovery, testabilidad y ejecución encubierta antes de versionar diseños técnicos.

## Estado

Regla creada.
