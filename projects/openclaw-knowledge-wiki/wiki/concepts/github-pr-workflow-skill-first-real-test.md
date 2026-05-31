# GitHub PR Workflow Skill — First Real Minimal Test

## Objetivo

Registrar la primera prueba real mínima guiada por la skill local `github-pr-workflow` v0.1.

La prueba valida únicamente la Fase 1 en workspace: crear documentación mínima dentro de OpenClaw Knowledge Wiki sin ejecutar Git ni copiar al repo limpio.

## Skill usada

```text
/openclaw/workspace/main/projects/openclaw-knowledge-wiki/skills/github-pr-workflow/SKILL.md
```

Estado de la skill:

```text
draft-local-only
```

## Modo

```text
real mínima / fase 1 workspace
```

## Alcance de Fase 1

Archivos permitidos:

```text
/openclaw/workspace/main/projects/openclaw-knowledge-wiki/wiki/concepts/github-pr-workflow-skill-first-real-test.md
/openclaw/workspace/main/projects/openclaw-knowledge-wiki/wiki/index.md
/openclaw/workspace/main/projects/openclaw-knowledge-wiki/wiki/log.md
```

## Límites

En esta fase no se permite:

- ejecutar Git;
- crear rama;
- copiar al repo limpio;
- hacer secret scan real;
- commit;
- push;
- PR;
- merge;
- modificar la skill;
- tocar `raw/`;
- tocar `~/.openclaw/skills`;
- tocar gateway, auth, tokens, systemd, `.env` ni logs crudos;
- escribir fuera del proyecto.

## Pasos esperados

1. Crear esta nota en `wiki/concepts/`.
2. Añadir la nota a `wiki/index.md`.
3. Añadir entrada append-only en `wiki/log.md`.
4. Validar por lectura directa que los tres archivos esperados existen o contienen la referencia.
5. Confirmar que no se tocó `raw/` ni Git.

## Qué no se automatiza

La skill no automatiza:

- creación de ramas;
- copias workspace → repo limpio;
- staging;
- commits;
- push;
- creación de PR;
- merge;
- validaciones de secretos reales;
- decisiones de autorización.

Cada fase posterior requiere autorización explícita de Albert.

## Fases pendientes

- Fase 2: validar workspace.
- Fase 3: preparar repo target limpio.
- Fase 4: copiar workspace → repo target.
- Fase 5: secret scan silencioso.
- Fase 6: diff review con rutas relativas Git.
- Fase 7: staging, commit y push solo con autorización separada.
- Fase 8: generar texto/URL de PR, sin `gh pr create` en MVP.

## Resultado

```text
Fase 1 creada y validada en workspace
```
