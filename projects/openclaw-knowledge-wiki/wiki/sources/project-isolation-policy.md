# Source Note — Project Isolation Policy

## Fuente

- `raw/docs/project-isolation-policy.md`

## Tipo

Política operativa interna no sensible sobre aislamiento de proyectos OpenClaw.

## Resumen

El documento define la política de aislamiento de proyectos OpenClaw.

La política busca evitar contaminación del core, cambios accidentales en servicios o rutas sensibles, y facilitar rollback y auditoría.

La regla central es que todo proyecto nuevo debe vivir dentro de:

```text
/openclaw/workspace/main/projects/<nombre-proyecto>/
```

## Datos confirmados

- El documento define la política de aislamiento de proyectos OpenClaw.
- El responsable operativo indicado es Neodaemon MAIN.
- El ámbito declarado es `/openclaw/workspace/main/projects/`.
- Todo proyecto nuevo debe crearse dentro de `/openclaw/workspace/main/projects/<nombre-proyecto>/`.
- Las rutas prohibidas incluyen core, scripts globales, systemd, RAG, memory, dashboard-v2, logs, backups, briefings, git_clean, `.env` y configuración OpenClaw de usuario.
- Solo Albert puede autorizar excepciones explícitas sobre rutas prohibidas.
- La autorización debe indicar ruta exacta, motivo, alcance, archivos afectados y rollback.
- Un proyecto aislado no puede escribir fuera de su propia carpeta.
- Un proyecto aislado no puede ejecutar scripts globales ni wrappers como `ru_event.sh` o `ru_interaction.sh`.
- `git add .` está prohibido desde `/openclaw/workspace/main`.
- Cualquier `git push` requiere autorización explícita de Albert.
- Los proyectos no pueden contener secretos, tokens, credenciales, `.env` reales, logs globales, memoria operativa, datos RAG internos ni dumps de Gmail/Telegram.
- El rollback esperado de un proyecto debe limitarse a eliminar o archivar su carpeta.
- Si hay duda sobre si una acción pertenece al proyecto o al core, debe tratarse como sensible y pedir confirmación explícita a Albert.

## Inferencias

- La política prioriza aislamiento, reversibilidad y trazabilidad sobre velocidad.
- La carpeta `projects/` funciona como frontera operativa entre experimentos/prototipos y el core de Neodaemon/OpenClaw.
- La prohibición de scripts globales reduce riesgo de acoplamiento accidental entre proyectos y operaciones centrales.
- El rollback por carpeta obliga a diseñar proyectos sin dependencias ocultas sobre core, logs o servicios.

## Dudas o límites

- La política permite excepciones con autorización explícita, pero no define un formato único de registro para esas excepciones.
- No especifica todavía un mecanismo técnico automático para impedir escrituras fuera del proyecto.
- La estructura mínima obliga `src/`, `data_samples/` y `exports/`, aunque algunos proyectos documentales pueden no necesitar esas carpetas.
- La política no sustituye a TASK_VALIDATOR ni a confirmación humana en acciones sensibles.

## Conceptos relacionados

- aislamiento de proyectos
- rutas prohibidas
- rollback por carpeta
- autorización explícita
- scripts globales
- datos prohibidos
- validación previa
- frontera project/core

## Enlaces internos

- `wiki/index.md`
- `wiki/log.md`
- `NEODAEMON_WIKI.md`
- `wiki/sources/first-source-openclaw-knowledge-wiki-readme.md`
