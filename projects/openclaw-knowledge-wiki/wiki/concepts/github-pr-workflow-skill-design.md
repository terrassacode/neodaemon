# GitHub PR Workflow Skill Design

## Propósito

Diseñar una skill local segura para ayudar a Neodaemon a repetir un flujo GitHub manual, reduciendo trabajo repetitivo sin convertirlo en autopilot.

La skill debe asistir en diagnóstico, checklist, preparación de salida y generación de texto de PR. No debe ejecutar commits, pushes, creación de PR ni merges en el MVP.

## Principio central

Una skill no es una barrera técnica real.

Si hay duda sobre repo, rama, rutas, secretos, estado de `main`, destino de copia o alcance de cambios, el resultado debe ser:

```text
BLOCK
```

## No objetivos

- No autopilot.
- No merge automático.
- No `gh pr create` en el MVP.
- No commit sin autorización explícita.
- No push sin autorización explícita.
- No tocar gateway, auth, tokens, systemd, `.env` ni logs crudos.
- No modificar `~/.openclaw/skills` en el MVP.
- No instalar skills reales en esta fase.

## Ubicación futura de la skill

No se decide todavía una ubicación definitiva.

Opciones futuras:

1. `project-local`: dentro del proyecto que documenta o usa el flujo.
2. `operational-skills`: ubicación operativa separada para skills internas validadas.

Regla MVP:

```text
No usar ~/.openclaw/skills en MVP.
```

## Estados del workflow

```text
S0_IDLE
S1_CONTEXT_CHECK
S2_REPO_VERIFY
S3_BRANCH_VERIFY
S4_MAIN_SYNC_VERIFY
S5_WORKTREE_CLEAN_VERIFY
S6_ALLOWED_PATHS_VERIFY
S7_COPY_PLAN
S8_SECRET_SCAN
S9_DIFF_REVIEW
S10_COMMIT_TEXT_READY
S11_PUSH_PLAN_READY
S12_PR_TEXT_READY
S13_WAIT_HUMAN_REVIEW
S_BLOCKED
```

Estado terminal permitido en MVP:

```text
PR text ready / URL suggested
```

Estado terminal prohibido:

```text
merge automático
```

## Validaciones obligatorias

Antes de cualquier fase no trivial, confirmar:

1. repo correcto;
2. rama correcta;
3. remoto correcto;
4. `main` verificado contra `origin/main`;
5. working tree limpio antes de copiar cambios;
6. rutas origen/destino explícitas;
7. allowlist de rutas aplicada;
8. rutas prohibidas descartadas;
9. secret scan silencioso ejecutado;
10. diff revisado antes de commit;
11. PR preparado con safety notes.

No asumir que GitHub `main` está actualizado sin verificar.

## Allowlist antes que blacklist

La skill debe operar solo sobre rutas explícitamente autorizadas por Albert.

Ejemplo de allowlist para operación documental:

```text
/openclaw/workspace/main/projects/openclaw-knowledge-wiki/wiki/concepts/
/openclaw/workspace/main/projects/openclaw-knowledge-wiki/wiki/index.md
/openclaw/workspace/main/projects/openclaw-knowledge-wiki/wiki/log.md
```

Todo lo que no esté en allowlist:

```text
BLOCK
```

## Rutas prohibidas por defecto

```text
/openclaw/.env
/home/openclaw/.openclaw/
/openclaw/workspace/main/.git/
/openclaw/workspace/main/logs/
/openclaw/workspace/main/systemd/
/openclaw/workspace/main/rag_store/
/openclaw/workspace/main/context_repo/personal/
/openclaw/workspace/main/backups/
/etc/
/var/log/
```

Matices importantes:

- `/tmp` está prohibido como destino de escritura o fuente Git.
- `/tmp` solo puede usarse para escaneo seguro read-only con autorización explícita.
- `/openclaw/bots` y `/openclaw/tools` están prohibidos por defecto.
- `/openclaw/bots` y `/openclaw/tools` solo son permitidos con autorización explícita de Albert y plan específico.

Patrones prohibidos por defecto:

```text
*.env
*.pem
*.key
*token*
*secret*
*credential*
```

## Secret scan ampliado y silencioso

Debe devolver solo:

```text
conteo
ruta
tipo de patrón
```

Nunca debe imprimir líneas coincidentes ni valores.

Patrones mínimos:

```text
api.telegram.org/bot
bot<digits>:<secret>
TELEGRAM_BOT_TOKEN
OPENAI_API_KEY
ANTHROPIC_API_KEY
GITHUB_TOKEN
ghp_
gho_
ghs_
BEGIN PRIVATE KEY
password=
token=
secret=
credential=
```

Si hay cualquier hallazgo:

```text
BLOCK
```

## Comandos permitidos como diagnóstico o propuesta

Solo se permiten como comandos propuestos o bajo autorización explícita por fase.

```bash
git status --short
git branch --show-current
git remote -v
git fetch origin
git rev-parse HEAD
git rev-parse origin/main
git log --oneline --decorate -n 5
git diff --stat
git diff -- <allowlisted-path>
git diff --cached --stat
git add <allowlisted-path>
git commit -m "<mensaje>"
git push origin <branch>
```

Condiciones:

- `git add` siempre con rutas explícitas.
- `git push` requiere autorización explícita de Albert.
- `git commit` requiere autorización explícita de Albert.
- `gh pr create` no se ejecuta en el MVP.
- El MVP solo genera URL sugerida y texto de PR.

## Comandos prohibidos

```bash
git add .
git add -A
git commit -am
git push --force
git push --force-with-lease
git reset --hard
git clean -fd
git merge
git rebase
gh pr create
gh pr merge
gh repo sync
```

También prohibido:

```text
sudo
docker
systemctl
openclaw gateway restart
edición de ~/.openclaw/skills
lectura de logs crudos
```

## Separación de fases

La skill debe separar claramente:

1. preparación de copia;
2. validación de rutas;
3. secret scan;
4. diff review;
5. preparación de commit;
6. commit autorizado;
7. preparación de push;
8. push autorizado;
9. generación de texto/URL de PR;
10. revisión humana;
11. merge humano fuera de la skill.

## Formato estándar de salida

```yaml
workflow_state: S9_DIFF_REVIEW
repo: /ruta/repo
branch: feature/...
base: main
main_status: verified_updated | unknown | stale
working_tree: clean | dirty | unknown
allowed_paths:
  - ...
blocked_paths:
  - ...
secret_scan:
  status: pass | fail | not_run
  findings_count: 0
risk_level: low | medium | high
requires_albert_authorization:
  - commit
  - push
  - pr_text_use
blocked_actions:
  - merge
  - gh_pr_create
next_recommended_action: ...
safe_to_execute: false
```

## PR description estándar

```markdown
## Summary

- ...

## Safety notes

- Scope limited to allowlisted paths.
- No gateway/auth/tokens/systemd/.env changes.
- No logs or raw secrets included.
- Secret scan: PASS/FAIL.
- Working tree before commit: clean/dirty.
- Base branch checked against origin/main.
- Merge automatic: prohibited.

## Validation

- [ ] File inspection
- [ ] Secret scan silent
- [ ] Diff reviewed
- [ ] Tests/lint if applicable

## Rollback

- Before commit: restore only explicit changed files.
- After commit: revert commit or abandon branch.
- After push: close PR or push revert commit.
```

## Puntos de autorización de Albert

Requieren confirmación explícita:

1. copiar archivos hacia repo destino;
2. `git add <path>`;
3. `git commit`;
4. `git push`;
5. usar texto/URL de PR generado;
6. cualquier cambio fuera de allowlist;
7. cualquier hallazgo de secret scan;
8. cualquier PR con riesgo medio/alto.

Nunca autorizado por la skill:

```text
merge automático
```

## Rollback por fase

- Antes de copiar: no-op.
- Después de copiar, antes de `git add`: restaurar archivo concreto desde copia conocida o descartar cambio manualmente.
- Después de `git add`: `git restore --staged <path>`.
- Después de commit local: `git revert <commit>` o abandonar rama.
- Después de push: revert commit + push nuevo, o cerrar PR.
- Después de PR: cerrar PR sin merge.
- Después de merge: fuera del MVP; requiere plan humano específico.

Regla explícita:

```text
No usar git reset --hard como rollback estándar.
```

## MVP recomendado

MVP documental/manual:

1. no instalar skill real;
2. no tocar `~/.openclaw/skills`;
3. no ejecutar GitHub CLI;
4. generar checklist;
5. generar comandos propuestos;
6. generar texto de commit;
7. generar texto de PR;
8. bloquear ante cualquier desviación.

## Riesgos residuales

- La skill no impide técnicamente que se ejecuten comandos peligrosos fuera del flujo.
- Una allowlist mal definida puede permitir cambios no deseados.
- Secret scan puede tener falsos negativos.
- Copiar desde workspace equivocado puede contaminar el repo.
- Un PR manual puede pegar texto incorrecto si no se revisa.
- `main` puede cambiar entre verificación y push.

## Decisión actual

Crear solo este diseño documental.

No crear skill real todavía.
No instalar nada.
No ejecutar Git.
No tocar `~/.openclaw/skills`.
