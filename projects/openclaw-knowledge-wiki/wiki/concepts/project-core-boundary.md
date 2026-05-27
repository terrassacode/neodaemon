# Project/Core Boundary

## Fuente

- `wiki/sources/project-isolation-policy.md`
- `wiki/sources/first-source-openclaw-knowledge-wiki-readme.md`
- `NEODAEMON_WIKI.md`
- `wiki/index.md`

## Resumen

La frontera project/core separa los proyectos aislados del núcleo operativo de Neodaemon/OpenClaw.

Un proyecto nuevo debe vivir dentro de:

```text
/openclaw/workspace/main/projects/<nombre-proyecto>/
```

La regla práctica es simple: si una acción escribe, ejecuta, modifica servicios, toca datos globales o afecta rutas fuera de la carpeta del proyecto, debe tratarse como sensible y requiere autorización explícita de Albert antes de ejecutarse.

## Datos confirmados

- Todo proyecto nuevo debe crearse dentro de `/openclaw/workspace/main/projects/<nombre-proyecto>/`.
- Un proyecto aislado no puede escribir fuera de su propia carpeta.
- Las rutas prohibidas incluyen core, scripts globales, systemd, RAG, memory, dashboard-v2, logs, backups, briefings, git_clean, `.env` y configuración OpenClaw de usuario.
- Un proyecto aislado no puede ejecutar scripts globales.
- Un proyecto aislado no puede invocar `ru_event.sh` ni `ru_interaction.sh`.
- `git add .` está prohibido desde `/openclaw/workspace/main`.
- Cualquier `git push` requiere autorización explícita de Albert.
- Las excepciones sobre rutas prohibidas requieren autorización explícita de Albert.
- Si hay duda sobre si una acción pertenece al proyecto o al core, debe tratarse como sensible y pedir confirmación explícita.
- OpenClaw Knowledge Wiki también mantiene aislamiento: no debe modificar `raw/`, no debe escribir fuera de su proyecto, no debe usar APIs externas, no debe instalar dependencias y no debe ejecutar scripts globales.

## Inferencias

- La carpeta `projects/` funciona como zona segura para experimentos, prototipos y aplicaciones.
- El core empieza, en términos operativos, cuando una acción toca rutas globales, servicios, scripts compartidos, memoria, RAG, dashboard operativo o configuración sensible.
- Una buena prueba de aislamiento es el rollback: si no puede revertirse eliminando solo la carpeta del proyecto, probablemente está contaminando el core.
- La frontera no depende solo de la ruta: ejecutar scripts globales desde un proyecto también rompe aislamiento.

## Dudas o límites

- La política permite excepciones autorizadas, pero no define aquí un formato único para registrar esas excepciones.
- Algunos proyectos documentales pueden no necesitar toda la estructura mínima de proyecto.
- Esta nota no sustituye a TASK_VALIDATOR ni a confirmación humana en acciones sensibles.
- No define mecanismos técnicos automáticos de bloqueo; es guía operacional derivada de las notas existentes.

## Checklist operativo

Antes de actuar dentro de un proyecto, comprobar:

- ¿La escritura queda dentro de la carpeta del proyecto?
- ¿Se evita tocar core, scripts globales, dashboard-v2, logs, memory, RAG, Gmail, Telegram, systemd y gateway?
- ¿No se ejecutan scripts globales ni wrappers como `ru_event.sh` o `ru_interaction.sh`?
- ¿No se usa `git add .` desde `/openclaw/workspace/main`?
- ¿No hay secretos, tokens, credenciales ni `.env` reales?
- ¿El rollback consiste solo en eliminar o archivar la carpeta del proyecto?
- Si hay duda, ¿se pide autorización explícita de Albert?

## Enlaces internos

- `wiki/sources/project-isolation-policy.md`
- `wiki/sources/first-source-openclaw-knowledge-wiki-readme.md`
- `NEODAEMON_WIKI.md`
- `wiki/index.md`
- `wiki/log.md`
