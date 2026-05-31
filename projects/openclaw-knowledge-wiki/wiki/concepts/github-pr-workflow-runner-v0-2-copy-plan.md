# GitHub PR Workflow Runner v0.2 — Copy Plan

## Propósito

Documentar el plan obligatorio antes de implementar `copy` automático controlado en `github_pr_workflow_runner.py` v0.2.

v0.2 ampliaría el runner desde:

```text
plan
check
```

hacia:

```text
plan
check
copy
```

sin introducir todavía Git write operations.

## Alcance permitido

v0.2 solo puede copiar archivos documentales permitidos por policy `DOCS_LOW_RISK`.

Rutas permitidas iniciales:

```text
projects/openclaw-knowledge-wiki/wiki/concepts/**
projects/openclaw-knowledge-wiki/wiki/index.md
projects/openclaw-knowledge-wiki/wiki/log.md
```

Debe bloquear:

```text
projects/openclaw-knowledge-wiki/raw/**
.env
**/.env
**/*token*
**/*secret*
**/*credential*
**/*.pem
**/*.key
logs/**
systemd/**
rag_store/**
context_repo/personal/**
.git/**
```

## Qué archivos puede copiar

Solo archivos que cumplan todos estos requisitos:

- ruta relativa permitida por `allowed_paths`;
- no coincide con `forbidden_paths`;
- extensión permitida: `.md`;
- encoding UTF-8;
- no binario;
- tamaño menor o igual a `max_file_bytes`;
- source dentro de workspace esperado;
- target dentro de repo target esperado;
- no symlink;
- sin path traversal;
- sin secretos detectados por secret scan silencioso.

## run_id único

Antes de cualquier operación de `copy`, v0.2 debe comprobar:

```text
automation/run_state/<run_id>/
```

Si ya existe:

```text
BLOCK
```

Excepción futura:

```text
recovery explícito documentado para el mismo run_id
```

Sin recovery explícito, reutilizar `run_id` queda prohibido para evitar mezclar snapshots, metadata, logs o rollback.

## Snapshot antes de sobrescribir

Antes de sobrescribir cualquier target:

1. crear carpeta de estado:
   ```text
   automation/run_state/<run_id>/
   ```

2. crear snapshot:
   ```text
   automation/run_state/<run_id>/snapshots/<git_relative_path>
   ```

3. crear metadata:
   ```text
   automation/run_state/<run_id>/metadata.json
   ```

4. registrar por archivo:
   - `git_relative_path`;
   - source relativo;
   - target relativo;
   - si target existía;
   - hash SHA-256 antes;
   - tamaño antes;
   - timestamp;
   - permisos básicos;
   - estado de validación.

Si el target no existía, registrar `existed=false` y no crear snapshot de contenido.

## Copy atómico

v0.2 no debe escribir directamente sobre el target.

Flujo obligatorio:

1. validar source;
2. validar target;
3. crear snapshot del target si existe;
4. copiar source a archivo temporal dentro de:
   ```text
   automation/run_state/<run_id>/tmp/
   ```
5. validar archivo temporal;
6. calcular hashes;
7. reemplazar target solo al final.

Si falla cualquier paso antes del replace:

```text
target queda intacto
```

Si falla después del replace:

```text
activar rollback por run_id usando snapshot
```

## Hash source before/after

Para detectar cambios concurrentes en el origen:

1. calcular `sha256_source_before` antes de copiar;
2. copiar source a temporal;
3. calcular `sha256_source_after` justo antes del replace;
4. comparar hashes.

Si cambia:

```text
BLOCK
```

No reemplazar target.

Registrar en metadata:

```json
{
  "sha256_source_before": "...",
  "sha256_source_after": "...",
  "source_changed_during_copy": false
}
```

## Tamaño antes de leer archivo completo

Antes de leer el archivo completo:

1. obtener tamaño mediante metadata del filesystem;
2. comparar contra `max_file_bytes`;
3. si supera límite:
   ```text
   BLOCK
   ```

Solo si el tamaño pasa el check se permite leer, copiar o escanear el contenido.

## Permisos no ejecutables

v0.2 no debe preservar permisos ejecutables.

Reglas:

- el target final debe ser archivo normal;
- el target final no debe ser ejecutable;
- no copiar bits ejecutables desde source;
- si source es ejecutable, bloquear o normalizar a no ejecutable según policy;
- para `DOCS_LOW_RISK`, recomendación: bloquear source ejecutable.

Validación posterior:

```text
target is regular file
target executable bit == false
```

## Cómo restaura si falla

Rollback conceptual por `run_id`:

- si el target existía: restaurar desde snapshot;
- si el target no existía: borrar archivo creado por el runner;
- no tocar archivos no listados en `run_state`;
- no usar `git reset --hard`;
- registrar resultado del rollback;
- si el archivo destino cambió después del snapshot, bloquear rollback automático y pedir revisión de Albert.

## Revalidación después de copiar

Después de copiar, v0.2 debe revalidar:

1. target existe;
2. target no es symlink;
3. realpath de target sigue dentro del repo target;
4. ruta relativa sigue dentro de allowlist;
5. ruta no coincide con forbidden paths;
6. extensión permitida;
7. encoding UTF-8;
8. no binario;
9. tamaño máximo;
10. hash SHA-256 después;
11. secret scan silencioso;
12. metadata actualizada;
13. run state consistente;
14. target es archivo normal no ejecutable.

Si cualquier check falla:

```text
BLOCK
```

## Cómo evita symlinks

Debe rechazar symlinks en:

- source;
- target existente;
- cualquier padre intermedio sospechoso si puede sacar la ruta fuera de raíz;
- snapshot path.

Validación mínima:

```text
is_symlink(source) == false
is_symlink(target) == false
realpath(source) dentro de workspace_root
realpath(target) dentro de repo_root
```

## Cómo evita path traversal

Debe bloquear:

```text
../
rutas absolutas como git_relative_paths
paths normalizados que salgan de workspace_root
paths normalizados que salgan de repo_root
```

Flujo obligatorio:

```text
input path
→ normalize
→ reject absolute git_relative_path
→ reject ..
→ resolve realpath
→ confirm inside expected root
→ confirm allowlist
→ confirm not forbidden
```

## Cómo mantiene run_state fuera de Git

`automation/.gitignore` debe ignorar:

```text
run_state/
approvals/
*.tmp
*.log
```

Antes de permitir `copy`, el runner debe comprobar que `run_state/` está ignorado por Git.

Si no puede confirmar que `run_state/` está ignorado:

```text
BLOCK
```

## Qué NO debe hacer v0.2

v0.2 no debe hacer:

```text
git add
commit
push
PR
merge
git reset --hard
force push
gh pr create
gh pr merge
```

Tampoco debe crear ramas automáticas salvo autorización explícita y fase separada.

## Checks contra branch y working tree

Antes de copiar, aunque v0.2 no haga commit:

- confirmar branch esperada si se usa repo target;
- bloquear si branch incorrecta;
- bloquear si working tree no está limpio;
- bloquear si hay cambios no relacionados.

Si no hay permiso para ejecutar diagnóstico Git read-only, entonces v0.2 debe bloquear copy.

## Logs sin secretos

Logs permitidos:

- estado;
- run_id;
- rutas relativas;
- conteos;
- tipos de hallazgo;
- hashes;
- tamaños;
- resultado de checks.

Logs prohibidos:

- valores secretos;
- líneas coincidentes de secret scan;
- URLs completas con token;
- contenido completo de archivos;
- stdout/stderr crudos no redactados.

## Snapshots y secretos

Riesgo: un snapshot puede contener secretos si el target previo ya estaba contaminado.

Mitigación:

- ejecutar secret scan silencioso sobre target antes de snapshot;
- si hay hallazgo, bloquear copy y no crear snapshot automático salvo plan específico;
- si snapshot ya existe y se detecta secreto, bloquear y pedir saneamiento seguro.

## Criterios de bloqueo

Bloquear si:

- `automation/run_state/<run_id>/` ya existe sin recovery explícito;
- source no está dentro de workspace esperado;
- target no está dentro de repo target;
- ruta no está allowlisted;
- ruta coincide con forbidden_paths;
- aparece `raw/`;
- path traversal detectado;
- symlink detectado;
- archivo no UTF-8;
- archivo binario;
- archivo demasiado grande;
- tamaño excede `max_file_bytes` antes de leer el contenido completo;
- extensión no permitida;
- secret scan detecta hallazgos;
- run_state no está ignorado por Git;
- working tree no está limpio;
- branch incorrecta;
- target cambió desde snapshot;
- source cambia entre `sha256_source_before` y `sha256_source_after`;
- copy temporal falla;
- archivo temporal no pasa validación;
- source o target tienen permisos ejecutables;
- target final no es archivo normal no ejecutable;
- hashes no coinciden con lo esperado;
- falta autorización por fase.

## Puntos ciegos específicos

- Qué pasa si el archivo destino ya existe y cambió desde el snapshot.
- Qué pasa si el archivo origen cambia durante la copia.
- Cómo verificar hash antes/después.
- Cómo impedir copiar archivos enormes.
- Cómo impedir binarios.
- Cómo tratar permisos de archivo.
- Cómo evitar copiar desde workspace equivocado.
- Cómo evitar escribir fuera del repo target.
- Cómo bloquear si `run_state/` no está ignorado por Git.
- Cómo detectar branch incorrecta.
- Cómo bloquear si working tree no está limpio antes de copiar.
- Cómo asegurar que solo se copian rutas relativas permitidas.
- Cómo registrar logs sin secretos.
- Cómo evitar que snapshots contengan secretos.
- Cómo hacer rollback sin `git reset --hard`.

## Riesgos

```text
medio
```

Motivo:

v0.2 introduce escritura de archivos en repo target mediante copy. Aunque no hay Git write operations, existe riesgo de sobrescritura accidental, copia fuera de allowlist, snapshot contaminado o rollback incompleto.

## Estado

Plan documental. No implementa copy real.
