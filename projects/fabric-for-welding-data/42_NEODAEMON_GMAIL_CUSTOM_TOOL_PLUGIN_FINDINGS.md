# 42_NEODAEMON_GMAIL_CUSTOM_TOOL_PLUGIN_FINDINGS.md

Status: DESIGN_LOOKUP_PARTIAL  
Fecha: 2026-05-23  
Relacionado con: `41_NEODAEMON_GMAIL_CONTROLLED_DRAFT_ACTION.md`

---

## 1. Objetivo

Documentar el hallazgo actual sobre cómo permitir que Neodaemon cree borradores Gmail directamente sin abrir `exec` general.

---

## 2. Conclusión actual

La vía recomendada sigue siendo:

```text
custom tool/plugin
```

y no:

```text
exec general
```

La acción deseada es:

```text
gmail_create_draft_controlled
```

---

## 3. Hallazgo parcial

La búsqueda disponible indica que OpenClaw soporta herramientas mediante plugins y control de exposición con:

```text
tools.allow
tools.deny
agents.list[].tools
```

No se ha confirmado todavía una clave declarativa simple tipo `argv` fijo sin plugin.

Por tanto, el mecanismo más probable es:

```text
crear un plugin local que registre una única tool parametrizada
```

---

## 4. Mecanismo probable

Diseño probable:

```text
1. Crear plugin local.
2. Registrar tool: gmail_create_draft_controlled.
3. Parámetros tipados:
   - to
   - subject
   - body
4. Ejecutar internamente argv fijo, sin shell.
5. Exponer solo esa tool al agente MAIN.
6. Mantener exec general denegado.
```

Argv objetivo:

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

## 5. Restricciones mantenidas

No permitir:

```text
exec general
shell libre
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
systemctl
journalctl
docker
node
npm
sendmail
```

No permitir llamadas Gmail de envío:

```text
users.messages.send
send_email
send_message
service.users().messages().send(
```

---

## 6. Estado actual de Gmail

Ya conseguido:

```text
PHASE_1_READONLY_WORKING
GMAIL_API_READONLY = WORKING
token.json creado e ignorado
client_secret.json creado e ignorado
```

Diseñado/preparado:

```text
PHASE_2_DRAFT_ONLY_DESIGN
PHASE_2_SCOPE_CANDIDATE = gmail.compose
PHASE_2_DRAFT_SCRIPT_PREPARED
CONTROLLED_ACTION_REQUIRED
```

Pendiente:

```text
confirmar mecanismo exacto de plugin custom
crear POC de plugin no-Gmail si procede
registrar tool controlada
exponer solo gmail_create_draft_controlled
```

---

## 7. Decisión operativa

No avanzar con `exec` general.

No seguir ampliando permisos del agente hasta confirmar mecanismo exacto de plugin/tool custom.

Próximo paso técnico recomendado:

```text
localizar documentación exacta de plugins/tools custom en OpenClaw
crear POC mínimo de plugin controlado antes de tocar Gmail
```

---

## 8. Estado final

```text
DOCUMENTED
CUSTOM_TOOL_PLUGIN_PROBABLE
NO_EXEC_GENERAL
NO_PLUGIN_IMPLEMENTED_YET
NO_NEW_PERMISSIONS_APPLIED
MAIN_INTACT
```
