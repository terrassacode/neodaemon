# GitHub PR Workflow Runner Design

## Propósito

Diseñar `github_pr_workflow_runner.py` como runner de automatización 100% controlada para cambios documentales de bajo riesgo.

El runner debe evolucionar gradualmente desde `plan/check` hacia ejecución automática completa solo para `DOCS_LOW_RISK`, con policy file, estados explícitos, checks estrictos, rollback por `run_id` y logs sin secretos.

Principio central:

```text
Si no encaja exactamente con policy + change_class + checks + estado esperado → BLOCK.
```

## Rutas propuestas

No crear todavía:

```text
projects/openclaw-knowledge-wiki/automation/github_pr_workflow_runner.py
projects/openclaw-knowledge-wiki/automation/policies/github_pr_workflow.policy.yml
projects/openclaw-knowledge-wiki/automation/run_state/
```

`automation/run_state/` debe quedar no versionado por defecto mediante `.gitignore` cuando se implemente.

## Alcance v0.1

v0.1 solo implementaría:

```text
plan
check
```

v0.1 no debe implementar:

```text
copy
commit
push
pr
merge
```

No existe comando `merge` en v0.1.

`allow_auto_commit`, `allow_auto_push` y `allow_auto_pr` son objetivo de madurez futura para `DOCS_LOW_RISK`, no comportamiento activo en runner v0.1.

Auto-merge queda solo como diseño futuro, no CLI activa.

## Policy YAML propuesta

```yaml
version: 0.1
default_safe_to_execute: false

paths:
  workspace_root: /openclaw/workspace/main
  repo_root: /openclaw/workspace/git_clean/neodaemon_repo
  run_state_dir: projects/openclaw-knowledge-wiki/automation/run_state

change_classes:
  DOCS_LOW_RISK:
    description: "Cambios documentales acotados, UTF-8, sin secretos ni código ejecutable."

    # Objetivos de madurez futura. No son comportamiento activo en runner v0.1.
    allow_auto_commit: true
    allow_auto_push: true
    allow_auto_pr: true
    allow_auto_merge: false

    allowed_paths:
      - projects/openclaw-knowledge-wiki/wiki/concepts/**
      - projects/openclaw-knowledge-wiki/wiki/index.md
      - projects/openclaw-knowledge-wiki/wiki/log.md

    forbidden_paths:
      - projects/openclaw-knowledge-wiki/raw/**
      - .env
      - "**/.env"
      - "**/*token*"
      - "**/*secret*"
      - "**/*credential*"
      - "**/*.pem"
      - "**/*.key"
      - logs/**
      - systemd/**
      - rag_store/**
      - context_repo/personal/**
      - .git/**

    allowed_extensions:
      - .md

    allowed_encodings:
      - utf-8

    max_files_changed: 3
    max_file_bytes: 200000
    max_added_lines: 300
    max_deleted_lines: 80

    reject_symlinks: true
    reject_binary: true
    reject_path_traversal: true
    require_realpath_inside_allowlist: true
    require_snapshot_before_copy: true
    require_append_only_log: true
    require_index_reference: true
    require_secret_scan: true
    require_diff_policy: true
    require_post_copy_revalidation: true

branching:
  base_branch: main
  branch_prefix: docs/
  branch_if_exists: block
  max_branch_length: 80

github:
  pr_labels:
    - docs
    - low-risk
  auto_merge:
    design_future_only: true
    enabled: false

commands:
  deny:
    - "git add ."
    - "git add -A"
    - "git push --force"
    - "git push --force-with-lease"
    - "git reset --hard"
    - "git clean -fd"
    - "git merge"
    - "git rebase"
    - "gh pr merge"
```

## Nota sobre patrones prohibidos y secret scan

Los patrones de nombre como `**/*token*`, `**/*secret*` o `**/*credential*` bloquean nombres de archivo y rutas.

Contenido tipo `token=`, claves, URLs de Bot API o valores secretos se evalúa mediante secret scan silencioso.

El secret scan nunca debe imprimir valores coincidentes.

## CLI propuesta

MVP v0.1:

```bash
python3 projects/openclaw-knowledge-wiki/automation/github_pr_workflow_runner.py plan \
  --policy projects/openclaw-knowledge-wiki/automation/policies/github_pr_workflow.policy.yml \
  --change-class DOCS_LOW_RISK \
  --repo /openclaw/workspace/git_clean/neodaemon_repo \
  --workspace /openclaw/workspace/main \
  --run-id <run_id>

python3 projects/openclaw-knowledge-wiki/automation/github_pr_workflow_runner.py check \
  --run-id <run_id>
```

Futuro controlado, no activo en v0.1:

```bash
python3 projects/openclaw-knowledge-wiki/automation/github_pr_workflow_runner.py copy \
  --run-id <run_id> \
  --approval-file approvals/<run_id>.approved.json
```

Alternativa sin secretos:

```bash
python3 projects/openclaw-knowledge-wiki/automation/github_pr_workflow_runner.py copy \
  --run-id <run_id> \
  --confirm-risk DOCS_LOW_RISK
```

No usar approval tokens secretos.

Futuro posible:

```text
commit
push
pr
```

No existe en v0.1:

```text
merge
```

## Estados del runner

```text
S0_INIT
S1_POLICY_LOADED
S2_INPUTS_NORMALIZED
S3_REPO_VERIFIED
S4_MAIN_SYNCED
S5_WORKTREE_CLEAN
S6_PATHS_VALIDATED
S7_SYMLINKS_REJECTED
S8_ENCODING_VALIDATED
S9_COPY_PLAN_CREATED
S10_SNAPSHOT_CREATED
S11_COPIED
S12_POST_COPY_REVALIDATED
S13_SECRET_SCAN_PASS
S14_DIFF_POLICY_PASS
S15_BRANCH_READY
S16_BRANCH_CREATED
S17_COMMIT_CREATED
S18_PUSHED
S19_PR_CREATED
S_BLOCKED
S_ROLLBACK_READY
S_ROLLED_BACK
```

No hay estado `MERGED` en v0.1.

## Checks obligatorios

### Repo

- repo path exacto;
- `.git` dentro del repo target;
- remote esperado;
- `origin/main` existe;
- `HEAD == origin/main` antes de branch;
- working tree limpio.

### Path traversal

Bloquear:

```text
../
rutas Git absolutas
paths fuera de repo/workspace esperados
paths normalizados que cambian de raíz
```

Flujo:

```text
normalize → reject absolute Git path → reject '..' → realpath → confirm inside expected root → confirm inside allowlist
```

### Symlinks

Regla:

```text
rechazar cualquier symlink en source o target
```

Checks:

- `is_symlink(source) == false`;
- `is_symlink(target) == false`;
- `realpath(source)` dentro del workspace esperado;
- `realpath(target)` dentro del repo esperado;
- `realpath(target)` sigue mapeando a allowlist relativa.

### Snapshot antes de copiar

Antes de sobrescribir target, crear snapshot en:

```text
projects/openclaw-knowledge-wiki/automation/run_state/<run_id>/snapshots/
```

Guardar:

- copia del target si existe;
- metadata JSON:
  - path relativo;
  - sha256 antes;
  - tamaño;
  - timestamp;
  - `existed: true/false`.

### Branch existente

Política:

```text
si branch existe local o remota → BLOCK
```

Excepción futura:

```text
recovery explícito con estado previo del mismo run_id
```

### Revalidación post-copy

Después de copiar:

1. `git status --short`;
2. changed paths exactos;
3. todos los changed paths dentro de allowlist;
4. secret scan silencioso;
5. diff policy;
6. encoding/tamaño otra vez;
7. no symlinks;
8. `raw/` intacto.

### Binarios / encoding

Para `DOCS_LOW_RISK` inicial:

```text
solo .md
UTF-8
sin symlinks
sin binarios
```

Bloquear:

- binarios;
- no UTF-8;
- extensión no permitida;
- archivo mayor que `max_file_bytes`;
- bytes nulos;
- archivos ejecutables;
- scripts.

## Comandos permitidos por estado

Diagnóstico:

```bash
git status --short
git branch --show-current
git remote -v
git fetch origin
git rev-parse HEAD
git rev-parse origin/main
git log --oneline --decorate -n 5
```

Diff:

```bash
git diff --stat
git diff -- <relative-path>
```

Futuro, no v0.1:

```bash
git checkout -b <generated-branch>
git add <explicit-relative-path>
git commit -m "docs: <summary>"
git push origin <generated-branch>
gh pr create --base main --head <generated-branch> --title "<title>" --body-file <body-file>
```

Prohibido siempre:

```bash
git add .
git add -A
git reset --hard
git clean -fd
git push --force
git push --force-with-lease
git merge
git rebase
gh pr merge
```

## Secret scan silencioso

Salida permitida:

```json
{
  "status": "fail",
  "findings": [
    {
      "path": "projects/...",
      "pattern_type": "TELEGRAM_BOT_TOKEN",
      "count": 1
    }
  ]
}
```

Prohibido:

```text
línea coincidente
valor secreto
URL completa
```

## Branch naming

```text
docs/<slug>-<YYYYMMDD>-<run_id_short>
```

Ejemplo:

```text
docs/github-pr-workflow-first-real-test-20260528-a1b2c3
```

Validar:

- solo `[a-z0-9._/-]`;
- máximo 80 caracteres;
- prefijo definido por policy;
- branch inexistente local y remotamente.

## run_state JSON

```json
{
  "run_id": "20260528-abc123",
  "change_class": "DOCS_LOW_RISK",
  "state": "S9_COPY_PLAN_CREATED",
  "policy_path": "projects/openclaw-knowledge-wiki/automation/policies/github_pr_workflow.policy.yml",
  "repo_root": "/openclaw/workspace/git_clean/neodaemon_repo",
  "workspace_root": "/openclaw/workspace/main",
  "run_state_dir": "projects/openclaw-knowledge-wiki/automation/run_state/20260528-abc123",
  "base_branch": "main",
  "branch": "docs/example-20260528-abc123",
  "source_paths": [],
  "target_paths": [],
  "git_relative_paths": [],
  "checks": {
    "repo_verified": false,
    "main_synced": false,
    "worktree_clean": false,
    "paths_validated": false,
    "symlinks_rejected": false,
    "encoding_validated": false,
    "snapshot_created": false,
    "post_copy_revalidated": false,
    "secret_scan": "not_run",
    "diff_policy": "not_run"
  },
  "artifacts": {
    "commit": null,
    "pr_url": null
  },
  "rollback": {
    "snapshot_dir": null,
    "copied_files": [],
    "created_branch": null,
    "created_commit": null,
    "created_pr": null
  }
}
```

## Logs sin secretos

Reglas:

- JSONL por `run_id`;
- redactar antes de escribir;
- no guardar stdout crudo de errores que puedan incluir URLs/token;
- secret scan guarda solo conteo/ruta/tipo;
- rutas preferentemente relativas;
- nunca valores coincidentes.

Ejemplo:

```json
{"run_id":"20260528-abc123","event":"secret_scan","status":"pass","findings_count":0}
```

## Rollback por run_id

- Antes de copy: no-op.
- Después de snapshot, antes de copy: borrar snapshot si se aborta.
- Después de copy: restaurar targets desde snapshot.
- Si target no existía: borrar archivo creado por runner.
- Después de branch: borrar branch local solo si fue creada por este run_id y no tiene push.
- Después de commit: revert commit o abandonar branch; no `reset --hard`.
- Después de push: cerrar PR si existe y push de revert commit si aplica.
- Después de PR: cerrar PR.
- Después de merge futuro: crear revert PR; nunca `reset --hard`.

## Límites duros

- No tocar `.env`.
- No tocar tokens/auth/gateway/systemd/logs crudos.
- No tocar `raw/`.
- No ejecutar scripts del proyecto.
- No instalar dependencias.
- No `sudo`.
- No Docker.
- No `git add .`.
- No force push.
- No auto-merge en v0.1.
- No comando `merge` en v0.1.

## Pruebas necesarias

1. parseo policy YAML;
2. path allowlist/forbidden;
3. path traversal;
4. symlink reject;
5. realpath containment;
6. UTF-8/binario;
7. tamaño máximo;
8. secret scan sin imprimir valores;
9. diff policy con archivos permitidos;
10. diff policy bloquea `raw/`;
11. bloqueo de `git add .`;
12. branch naming válido;
13. branch existente local/remota bloquea;
14. snapshot antes de copy;
15. revalidación post-copy;
16. run state transitions;
17. rollback plan por estado;
18. log redaction;
19. dry-run completo `DOCS_LOW_RISK`;
20. test con repo temporal.

## Riesgos residuales

```text
medio
```

Motivos:

- full-auto con Git/GitHub siempre tiene riesgo operacional;
- secret scan puede tener falsos negativos;
- policy mal escrita puede permitir rutas indebidas;
- symlink/path traversal reduce riesgo pero debe testearse bien;
- auto-merge futuro debe permanecer desactivado hasta madurez alta.

## Plan de implementación

1. Documentar diseño corregido.
2. Crear `.gitignore` futuro para `automation/run_state/`.
3. Crear policy YAML de ejemplo.
4. Implementar runner v0.1 solo:
   - `plan`;
   - `check`;
   - sin copy real.
5. Tests unitarios:
   - policy parse;
   - allowlist/forbidden;
   - path traversal;
   - symlink reject;
   - realpath containment;
   - UTF-8/binario;
   - branch naming;
   - run_state transitions;
   - log redaction.
6. Implementar snapshot + copy en v0.2 con approval file.
7. Implementar commit/push en v0.3.
8. Implementar PR en v0.4.
9. Evaluar auto-merge solo como diseño futuro, no CLI activa.

## Estado actual

```text
Diseño documental creado. No existe runner real, policy real, .gitignore ni run_state.
```
