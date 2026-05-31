# GitHub PR Workflow Skill — Dry-run conceptual v2

## Contexto

Se realizó una simulación conceptual de la skill local `github-pr-workflow` v0.1 para validar que distingue correctamente entre:

1. origen de trabajo en workspace;
2. destino versionable en repo limpio;
3. rutas relativas correctas para operaciones Git.

## Skill evaluada

```text
/openclaw/workspace/main/projects/openclaw-knowledge-wiki/skills/github-pr-workflow/SKILL.md
```

Estado:

```text
draft-local-only
```

No instalada globalmente.  
No activada en `~/.openclaw/skills`.

## Caso simulado

Añadir una futura nota documental simple:

```text
future-test-note.md
```

## Workspace source paths

Rutas simuladas de origen de trabajo:

```text
/openclaw/workspace/main/projects/openclaw-knowledge-wiki/wiki/concepts/future-test-note.md
/openclaw/workspace/main/projects/openclaw-knowledge-wiki/wiki/index.md
/openclaw/workspace/main/projects/openclaw-knowledge-wiki/wiki/log.md
```

## Repo target paths

Rutas simuladas de destino versionable en repo limpio:

```text
/openclaw/workspace/git_clean/neodaemon_repo/projects/openclaw-knowledge-wiki/wiki/concepts/future-test-note.md
/openclaw/workspace/git_clean/neodaemon_repo/projects/openclaw-knowledge-wiki/wiki/index.md
/openclaw/workspace/git_clean/neodaemon_repo/projects/openclaw-knowledge-wiki/wiki/log.md
```

## Git relative paths

Rutas correctas para `git diff` / `git add` desde el repo target:

```text
projects/openclaw-knowledge-wiki/wiki/concepts/future-test-note.md
projects/openclaw-knowledge-wiki/wiki/index.md
projects/openclaw-knowledge-wiki/wiki/log.md
```

## Branch sugerida

```text
docs/future-test-note
```

## Comandos plantilla correctos

Desde el repo target:

```bash
cd /openclaw/workspace/git_clean/neodaemon_repo
```

Plantillas diagnósticas:

```bash
git status --short
git branch --show-current
git remote -v
git fetch origin
git rev-parse origin/main
git diff --stat
git diff -- projects/openclaw-knowledge-wiki/wiki/concepts/future-test-note.md
git diff -- projects/openclaw-knowledge-wiki/wiki/index.md
git diff -- projects/openclaw-knowledge-wiki/wiki/log.md
```

Plantillas solo con autorización posterior de Albert:

```bash
git add projects/openclaw-knowledge-wiki/wiki/concepts/future-test-note.md
git add projects/openclaw-knowledge-wiki/wiki/index.md
git add projects/openclaw-knowledge-wiki/wiki/log.md
git commit -m "docs: add future test note"
git push origin docs/future-test-note
```

## Bloqueos correctos

La simulación bloquea correctamente:

- usar rutas absolutas en `git add`;
- confundir workspace source con repo target;
- usar `/openclaw/workspace/main` como repo target;
- `git add .`;
- `git add -A`;
- `gh pr create`;
- merge;
- force push;
- `git reset --hard`;
- lectura de logs crudos;
- tocar `.env`, tokens, auth, gateway o systemd;
- continuar si `main` no está verificado contra `origin/main`;
- continuar si working tree no está limpio antes de copiar;
- continuar con hallazgos de secret scan sin revisión de Albert;
- continuar sin autorización por fase.

## Puntos de autorización Albert

La skill debe pedir autorización explícita para:

1. confirmar repo target limpio;
2. confirmar branch `docs/future-test-note`;
3. autorizar copia workspace → repo target;
4. autorizar secret scan silencioso;
5. autorizar diff review;
6. autorizar cada `git add <ruta>`;
7. autorizar commit;
8. autorizar push;
9. autorizar uso manual de texto/URL de PR.

## Resultado

```text
APROBADO
```

La skill `github-pr-workflow` v0.1 distingue correctamente:

- `workspace_source_paths`;
- `repo_target_paths`;
- `git_relative_paths`.

También mantiene bloqueo por defecto y separación por fases.

## Límites

No se ejecutó nada.

No hubo:

- creación de archivos;
- copia workspace → repo;
- comandos Git;
- creación de rama;
- secret scan real;
- commit;
- push;
- PR;
- merge;
- instalación de skill;
- cambios en `~/.openclaw/skills`.

## Estado final

```yaml
workflow_state: S_BLOCKED
mode: dry-run-conceptual-v2
result: approved
safe_to_execute: false
```
