# Human Approval GitHub Executor v0.1

## Estado

Documento de diseño de meta-workflow.

Clasificación según `docs/protected-zones-blacklist-v0-1.md`:

```text
SPECIAL_CONFIRMATION
```

Este documento diseña un executor seguro para asistir el Human Approval GitHub Workflow. No implementa código.

## Objetivo

Definir un executor local y restringido que permita a Neodaemon operar trabajo Git local de forma controlada, sin shell libre y respetando el flujo de aprobación humana.

El executor v0.1 debe permitir trabajo local bajo `OK FEATURE` o `CONFIRMACIÓN_ESPECIAL`, pero no debe publicar en GitHub.

## Documentos normativos

El executor debe obedecer siempre:

- `docs/protected-zones-blacklist-v0-1.md`
- `docs/human-approval-github-workflow-v0-1.md`

Precedencia obligatoria:

```text
BLACKLIST > WORKFLOW > FEATURE > EXECUTOR
```

Si hay conflicto, gana la blacklist.

---

## Principio principal

```text
Albert valida decisiones; Neodaemon valida técnica; el executor limita ejecución.
```

El executor no decide por sí mismo.

El executor solo ejecuta acciones permitidas, parametrizadas y validadas.

---

## Alcance v0.1 — LOCAL ONLY

Executor v0.1 es estrictamente local.

Permitido:

- status;
- diff;
- create branch;
- validate;
- stage explicit files;
- commit.

Prohibido en v0.1:

- push;
- PR;
- `gh`;
- auth;
- tokens;
- red;
- APIs externas;
- `curl`;
- `wget`.

Cualquier intento de añadir estas capacidades al v0.1 debe producir:

```text
FEATURE_BLOCKED
```

o requerir aprobación especial futura fuera de este documento.

---

## Capacidades mínimas

### Read-only permitidas sin interacción humana

Las lecturas seguras no cuentan como interacción humana si se aplican sobre el repo permitido y rutas no sensibles:

```text
status
diff-stat
diff-name-only
diff
current-branch
log-oneline
file-exists
show-file-range
```

Equivalencias permitidas:

```text
git status --short
git branch --show-current
git log --oneline
git diff --stat
git diff --name-only
git diff
test -f <archivo_previsto>
sed -n '<rango>p' <archivo_previsto>
grep <patrón_seguro> <archivo_previsto>
```

Restricciones:

- solo rutas previstas o no sensibles;
- nunca sobre `.env`, logs, backups, snapshots, sessions, tokens, auth o credentials;
- salida sanitizada si puede contener secretos;
- sin pipes arbitrarios;
- sin comandos compuestos.

### Escritura local permitida tras aprobación

Solo tras `OK FEATURE` o `CONFIRMACIÓN_ESPECIAL`, según clasificación:

```text
create-branch
write-planned-file
validate-files
stage-explicit-files
commit-feature
```

Equivalencias permitidas:

```text
git checkout main
git pull origin main
git checkout -b <branch>
python3 -m py_compile <archivo.py>
bash -n <archivo.sh>
git add <archivo_concreto>
git commit -m "<mensaje>"
```

Cada acción debe validar rutas, estado Git y blacklist antes de ejecutarse.

---

## Repo Root Lock

El executor debe operar solo dentro del repo aprobado.

### Allowed repositories

El executor v0.1 solo puede operar sobre repositorios incluidos explícitamente en esta allowlist.

Repositorios permitidos:

```text
/openclaw/workspace/git_clean/neodaemon_repo
```

Ningún otro repositorio, worktree o ruta Git queda permitido por defecto.

Si se solicita operar sobre un repositorio no incluido en la allowlist:

```text
FEATURE_BLOCKED
```

Motivo:

```text
repository_not_allowed
```

Reglas:

1. Resolver `realpath` del repo root antes de cualquier acción.
2. Resolver `realpath` de cada ruta objetivo.
3. Bloquear cualquier ruta que escape del repo root.
4. Bloquear symlinks que apunten fuera del repo root.
5. Bloquear rutas absolutas no permitidas.
6. Bloquear `..` si produce escape del repo.
7. Bloquear operaciones si el repo root no coincide exactamente con el configurado.

Ante escape o duda:

```text
FEATURE_BLOCKED
```

Motivo:

```text
repo_root_lock_violation
```

---

## Output Size Guard

El executor debe evitar generar o mostrar salidas excesivas.

Motivo: diffs, logs o lecturas largas pueden consumir contexto excesivo o exponer información sensible.

Límites v0.1 recomendados:

```text
max_stdout_bytes_per_command: 20000
max_diff_files: 20
max_diff_bytes: 50000
max_file_read_bytes: 20000
max_file_read_lines: 300
```

Reglas:

- si la salida excede límite, truncar y marcar `truncated: true`;
- si el diff excede el límite, bloquear antes de commit;
- si hay más archivos modificados de los previstos, bloquear;
- no imprimir contenido sensible aunque esté dentro del límite;
- para archivos grandes, mostrar resumen metadata y pedir revisión especial.

Bloqueo:

```text
FEATURE_BLOCKED
```

Motivo:

```text
output_size_guard_exceeded
```

---

## No Auto-Discovery

El executor no debe descubrir automáticamente nuevos archivos para modificar, stagear o validar.

Reglas:

1. Los archivos modificables deben venir de `FEATURE_PROPOSAL`.
2. Los archivos stageables deben venir de `FEATURE_PROPOSAL`.
3. El executor no puede usar patrones amplios para añadir archivos.
4. El executor no puede convertir archivos detectados por `git status` en permitidos automáticamente.
5. Si aparece un archivo no previsto, bloquear.
6. Si aparece un archivo generado, bloquear salvo generador explícitamente autorizado.

Prohibido:

```text
git add .
git add -A
git add *
git add docs/
git add <directorio>
```

Permitido solo:

```text
git add <archivo_concreto_previsto>
```

Bloqueo:

```text
FEATURE_BLOCKED
```

Motivo:

```text
unexpected_file_or_auto_discovery
```

---

## Protected Zones / Denylist

El executor debe aplicar `docs/protected-zones-blacklist-v0-1.md` antes de cualquier acción.

### BLOCK por defecto

- Core OpenClaw;
- secrets/credentials;
- logs/backups/snapshots/sessions;
- escritura manual en generated data;
- protected project raw zones;
- services/system automation;
- integraciones externas;
- comandos prohibidos.

### SPECIAL_CONFIRMATION mínimo

- Human Approval documents;
- protected-zones documents;
- meta-workflow;
- github executor;
- workflow engine;
- task validator;
- approval policies;
- security policies;
- package locks / dependency surface;
- Docker/runtime environment.

### ALLOWED_ONLY_IF_EXPLICIT

- scripts `.py` / `.sh`;
- generadores autorizados;
- rutas de riesgo medio explícitamente previstas.

Si una ruta coincide con varias reglas, se aplica la más restrictiva.

---

## Executor Scope Lock

El executor no puede modificar su propio alcance o permisos mediante feature ordinaria.

Requieren `SPECIAL_CONFIRMATION` mínimo:

- diseño del executor;
- implementación del executor;
- allowlists;
- denylists;
- rutas permitidas;
- rutas prohibidas;
- comandos permitidos;
- comandos prohibidos;
- validaciones obligatorias;
- política de logs;
- política de secretos;
- reglas de bloqueo.

Debe bloquear si se intenta introducir sin aprobación especial:

```text
push
PR creation
gh
auth
token handling
network access
GitHub API
force push
auto-merge
systemd/cron/timers
service modification
```

Motivo:

```text
executor_scope_lock_violation
```

---

## Comandos prohibidos siempre

```text
git add .
git add -A
git commit -am
git push origin main
git push --force
git push --force-with-lease
git merge
git rebase
git reset --hard
git clean -fd
gh pr merge
sudo
curl
wget
docker
systemctl
crontab
```

También prohibido:

- shell libre;
- `shell=True`;
- comandos compuestos;
- pipes arbitrarios;
- redirecciones arbitrarias;
- backticks;
- `$()`;
- ejecución de scripts no previstos;
- lectura de rutas sensibles.

---

## Diseño técnico esperado

Cuando se implemente en una fase futura, el executor debe:

- usar listas de argumentos, nunca strings shell;
- usar `subprocess.run(..., shell=False)`;
- tener allowlist cerrada de acciones;
- validar repo root antes de cada acción;
- validar rutas antes de cada acción;
- aplicar denylist antes de allowlist;
- aplicar output size guard;
- no guardar prompts/respuestas;
- no guardar tokens;
- registrar solo metadata mínima;
- devolver errores estructurados;
- fallar cerrado.

Ejemplo conceptual de salida:

```json
{
  "ok": true,
  "action": "diff-stat",
  "risk": "low",
  "blocked": false,
  "truncated": false
}
```

Ejemplo conceptual de bloqueo:

```json
{
  "ok": false,
  "action": "stage-explicit-files",
  "blocked": true,
  "reason": "unexpected_file_or_auto_discovery",
  "next": "FEATURE_BLOCKED"
}
```

---

## Flujo v0.1

### 1. Precheck

- confirmar repo root;
- confirmar rama actual;
- confirmar `main` limpio y actualizado;
- confirmar working tree limpio;
- confirmar archivos previstos;
- aplicar blacklist;
- estimar riesgo.

### 2. Aprobación humana

Según clasificación:

- `OK FEATURE` para feature normal;
- `CONFIRMACIÓN_ESPECIAL` para meta-workflow o zonas especiales.

### 3. Trabajo local

- crear rama;
- modificar solo archivos previstos;
- validar;
- revisar diff;
- stage explícito;
- commit.

### 4. Resultado

Presentar `FEATURE_READY_FOR_GITHUB` si el trabajo local queda listo.

El executor v0.1 no ejecuta `OK GITHUB`; solo prepara el estado local.

---

## Acciones GitHub fuera de alcance v0.1

Quedan para fase futura:

- `push-branch`;
- `create-pr`.

Estas acciones no pertenecen al executor v0.1.

Fase futura requerirá nuevo diseño y aprobación especial.

---

## Manejo de tokens

Executor v0.1 no maneja tokens.

Prohibido:

- leer tokens;
- imprimir tokens;
- guardar tokens;
- aceptar token como argumento;
- aceptar token por env;
- escribir token en remoto Git;
- usar `gh auth`;
- usar GitHub API.

Si aparece una necesidad de autenticación:

```text
FEATURE_BLOCKED
```

---

## Riesgos

1. Convertir el wrapper en shell indirecta.
2. Permitir rutas amplias que evadan la blacklist.
3. Imprimir diffs demasiado grandes o sensibles.
4. Stagear archivos no previstos.
5. Ampliar capacidades GitHub antes de tiempo.
6. Modificar el propio workflow sin confirmación especial.

Mitigaciones:

- local-only;
- repo root lock;
- output size guard;
- no auto-discovery;
- executor scope lock;
- blacklist primero;
- fail closed.

---

## Criterios mínimos antes de implementar PR futuro

Antes de crear `scripts/github_workflow_executor.py`, debe existir:

1. PR de blacklist merged.
2. PR de este diseño merged.
3. Confirmación especial para código ejecutable.
4. Tests del executor diseñados antes de ampliar capacidades.
5. SELF_CHECK_PYTHON obligatorio.

---

## Estado final v0.1

Este documento solo diseña el executor.

No autoriza:

- implementación;
- push;
- PR;
- GitHub auth;
- red;
- APIs externas;
- tokens;
- servicios;
- automatización persistente.
