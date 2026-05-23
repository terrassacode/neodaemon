# 41_NEODAEMON_GMAIL_CONTROLLED_DRAFT_ACTION.md

Status: DESIGN_ONLY  
Capability: `gmail_create_draft_controlled`  
Cuenta: `claw.neodaemon@gmail.com`  
Fecha: 2026-05-23  
Relacionado con:

- `38_NEODAEMON_GMAIL_PHASE2_DRAFT_ONLY_DESIGN.md`
- `39_NEODAEMON_GMAIL_PHASE2_SCOPE_DECISION.md`
- `40_NEODAEMON_GMAIL_PHASE2_DRAFT_SCRIPT_PREPARED.md`

---

## 1. Objetivo

Definir una acción controlada para que Neodaemon pueda crear borradores Gmail directamente sin recibir `exec` general ni acceso libre a shell.

La acción propuesta permite:

```text
crear borradores Gmail
```

pero no permite:

```text
enviar correos
ejecutar shell libre
modificar labels
borrar correos
archivar
descargar adjuntos
tocar gateway/runtime/servicios
```

---

## 2. Decisión principal

No se debe habilitar `exec` general para MAIN.

Se debe implementar, si OpenClaw lo permite, una acción cerrada y parametrizada:

```text
gmail_create_draft_controlled
```

Regla:

```text
Neo no ejecuta shell. Neo invoca una acción cerrada para drafts().create.
```

---

## 3. Riesgo

Clasificación:

```text
CONTROLLED_SINGLE_COMMAND_CAPABILITY
risk: medio
```

Motivo:

- la acción crea borradores reales en Gmail;
- toca un sistema externo;
- no envía correos;
- no modifica buzón fuera de borradores;
- no borra ni archiva;
- requiere confirmación explícita de Albert antes de ejecutarse.

---

## 4. Acción permitida

Nombre sugerido:

```text
gmail_create_draft_controlled
```

Propiedades:

```text
working_dir: /openclaw/workspace/addons/gmail-readonly
venv: /openclaw/workspace/addons/gmail-readonly/.venv
script: /openclaw/workspace/addons/gmail-readonly/gmail_draft_check.py
args: ["<to>", "<subject>", "<body>"]
requires_confirmation: true
timeout: 30s
stdout_redaction: enabled
stderr_redaction: enabled
```

Preferencia técnica:

```text
usar argv fijo, no shell
```

Ejemplo de argv permitido:

```text
cwd=/openclaw/workspace/addons/gmail-readonly
argv=[
  "/openclaw/workspace/addons/gmail-readonly/.venv/bin/python",
  "/openclaw/workspace/addons/gmail-readonly/gmail_draft_check.py",
  "<to>",
  "<subject>",
  "<body>"
]
```

---

## 5. Comandos explícitamente denegados

No permitir:

```text
bash
sh
python -c
pip
curl
wget
git
rm
mv
cp
openclaw gateway *
systemctl
journalctl
docker
node
npm
sendmail
```

No permitir ejecuciones que contengan:

```text
users.messages.send
send_email
send_message
service.users().messages().send(
labels().*
trash
delete
modify
attachments
```

---

## 6. Preflight obligatorio

Antes de ejecutar la acción, validar estáticamente:

```bash
python -m py_compile gmail_draft_check.py
grep -nE 'users\.messages\.send|send_email|send_message|service\.users\(\)\.messages\(\)|\.send\(' gmail_draft_check.py || true
grep -n 'drafts().create' gmail_draft_check.py
```

Resultado esperado:

```text
py_compile: OK
grep peligroso: sin coincidencias
drafts().create: presente
```

Si aparece una coincidencia peligrosa, no ejecutar.

---

## 7. Confirmación humana

Antes de crear un borrador, Neodaemon debe mostrar:

```text
Acción: crear borrador Gmail
Cuenta: claw.neodaemon@gmail.com
Destinatario:
Asunto:
Cuerpo final:
Adjuntos: ninguno
Riesgos detectados:
```

Albert debe confirmar explícitamente:

```text
CONFIRMO CREAR BORRADOR
```

Sin esta confirmación, la acción no se ejecuta.

---

## 8. Salida permitida

Después de ejecutar, mostrar solo:

```text
draft_created: true
draft_id: <id>
```

No imprimir:

```text
token.json
token_compose.json
client_secret.json
refresh_token
access_token
.env
cuerpo completo si no hace falta
```

---

## 9. Rollback

Si algo falla:

1. Deshabilitar `gmail_create_draft_controlled`.
2. Volver a estado `PHASE_1_READONLY_WORKING`.
3. Revocar OAuth compose desde Google Account si hay sospecha de abuso.
4. Borrar `token_compose.json` local si se decide invalidar Fase 2.
5. Mantener `token.json` read-only y `token_readonly.backup.json` intactos salvo decisión explícita.

Si se crea un borrador por error:

```text
no borrarlo automáticamente
pedir confirmación explícita a Albert
borrarlo manualmente desde Gmail o mediante acción futura específica
```

---

## 10. Estado final de este documento

```text
DESIGN_ONLY
NO_EXEC_GENERAL
CONTROLLED_ACTION_REQUIRED
NO_SEND
NO_DELETE
NO_MODIFY_LABELS
NO_ATTACHMENTS
MAIN_INTACT
```
