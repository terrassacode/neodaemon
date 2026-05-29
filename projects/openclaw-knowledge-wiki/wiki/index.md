# OpenClaw Knowledge Wiki — Index

Catálogo maestro de notas generadas por Neodaemon.

## Estado

Segundo ingest manual ejecutado.

## Secciones

- `concepts/`: conceptos explicados y conectados.
- `entities/`: personas, proyectos, módulos o sistemas relevantes.
- `sources/`: resúmenes trazables de fuentes.
- `comparisons/`: comparativas entre enfoques, herramientas o decisiones.

## Notas

- `sources/first-source-openclaw-knowledge-wiki-readme.md` — resumen trazable del README del propio proyecto.
- `sources/project-isolation-policy.md` — resumen trazable de la política de aislamiento de proyectos OpenClaw.
- `concepts/project-core-boundary.md` — nota conceptual sobre la frontera operativa entre proyectos aislados y core OpenClaw.
- `concepts/obsidian-operating-rules.md` — reglas operativas para usar Obsidian como visor/editor local sin romper aislamiento.
- `concepts/github-pr-workflow-skill-design.md` — diseño de una skill local segura para asistir flujos GitHub PR manuales sin autopilot.
- `concepts/github-pr-workflow-skill-dry-run-v2.md` — registro del dry-run conceptual v2 de la skill `github-pr-workflow`, validando separación entre workspace source, repo target y rutas Git relativas.
- `concepts/github-pr-workflow-skill-first-real-test.md` — registro de la primera prueba real mínima de la skill `github-pr-workflow`, limitada a Fase 1 workspace.
- `concepts/github-pr-workflow-runner-design.md` — diseño técnico corregido del runner `github_pr_workflow_runner.py` para automatización 100% controlada de `DOCS_LOW_RISK`.
- `concepts/python-code-self-check-rule.md` — regla obligatoria `SELF_CHECK_PYTHON` para revisar código Python antes de proponerlo o crearlo.
- `concepts/github-pr-workflow-runner-v0-2-copy-plan.md` — plan técnico obligatorio para implementar `copy` controlado con snapshot, copy atómico y revalidación en runner v0.2.
- `concepts/design-doc-check-rule.md` — regla obligatoria `DESIGN_DOC_CHECK` para revisar calidad documental, evidencia, contradicciones, límites y ejecución encubierta antes de versionar diseños técnicos.
- `concepts/repo-root-inventory-and-risk-map.md` — mapa de inventario y riesgos de la raíz del repositorio, con dependencias confirmadas antes de cualquier reestructuración.
- `concepts/root-api-backup-security-review.md` — revisión de seguridad pendiente sobre archivos API heredados en la raíz con posibles tokens hardcodeados.
- `concepts/neodaemon-strategic-roadmap.md` — roadmap estratégico que redefine Neodaemon como operador confiable y separa razonamiento, gobernanza, automatización GitHub y profesionalización del repositorio.
- `concepts/task-validator-roadmap.md` — roadmap operativo para convertir `TASK_VALIDATOR` en router de riesgo, con niveles de contexto, control de tokens, criterios de bloqueo y relación con el runner GitHub.
- `concepts/dependency-checker-roadmap.md` — roadmap para convertir `DEPENDENCY_CHECKER` en analizador de impacto con modos TARGET/MAP, niveles D0-D3, clasificación de referencias y control de contexto.

## Fuentes registradas

- `raw/notes/first-source-openclaw-knowledge-wiki-readme.md` — copia inmutable de `README.md`.
- `raw/docs/project-isolation-policy.md` — copia inmutable de `PROJECT_ISOLATION_POLICY.md`.

## Pendiente

- Revisar si el nivel de detalle de la nota generada es útil.
- Mantener máximo 3 fuentes por ingest.
- Revisar el segundo ingest mediante lint manual.
- Revisar la nota conceptual `project-core-boundary.md` mediante lint manual.
- Revisar la nota conceptual `obsidian-operating-rules.md` mediante lint manual.
- Revisar la nota conceptual `github-pr-workflow-skill-design.md` mediante lint manual.
- Revisar la nota conceptual `github-pr-workflow-skill-dry-run-v2.md` mediante lint manual.
- Validar la Fase 1 de `github-pr-workflow-skill-first-real-test.md`.
- Revisar la nota conceptual `github-pr-workflow-runner-design.md` mediante lint manual.
- Revisar la nota conceptual `python-code-self-check-rule.md` mediante lint manual.
- Revisar la nota conceptual `github-pr-workflow-runner-v0-2-copy-plan.md` mediante lint manual.
- Definir próxima fuente no sensible.
