# 39_NEODAEMON_GMAIL_PHASE2_SCOPE_DECISION.md

Status: PHASE_2_SCOPE_DECISION  
Cuenta: `claw.neodaemon@gmail.com`  
Fecha: 2026-05-23  
Relacionado con: `38_NEODAEMON_GMAIL_PHASE2_DRAFT_ONLY_DESIGN.md`

---

## 1. Objetivo

Registrar la decisión preliminar sobre el scope OAuth necesario para Fase 2 Gmail Draft-only.

Este documento no activa OAuth nuevo ni modifica el addon.

---

## 2. Decisión preliminar

Scope candidato para Fase 2:

```text
https://www.googleapis.com/auth/gmail.compose
```

Motivo:

- permite crear y gestionar borradores;
- evita usar `gmail.modify` para operaciones generales del buzón;
- evita usar `https://mail.google.com/`, que daría acceso demasiado amplio.

---

## 3. Advertencia crítica

Aunque la fase se llame Draft-only, `gmail.compose` puede permitir enviar mensajes creados por la aplicación.

Por tanto, la seguridad no depende solo del scope OAuth.

Debe reforzarse con política y código:

- no implementar función de envío;
- no llamar a `users.messages.send`;
- no exponer ninguna acción `send`;
- permitir solo `users.drafts.create`, `users.drafts.get`, `users.drafts.list` y, si se aprueba, `users.drafts.update`;
- exigir confirmación explícita antes de crear o actualizar borradores.

---

## 4. Scopes descartados para esta fase

No usar en Fase 2:

```text
https://www.googleapis.com/auth/gmail.modify
https://www.googleapis.com/auth/gmail.send
https://mail.google.com/
```

Motivo:

- `gmail.modify` abre modificación general del buzón;
- `gmail.send` está orientado a envío;
- `mail.google.com` equivale a acceso muy amplio y no respeta mínimo privilegio.

---

## 5. Requisitos antes de implementación

Antes de tocar el addon:

- revisar documentación oficial si es necesario;
- confirmar que `gmail.compose` es el scope mínimo aceptable;
- documentar rollback OAuth;
- revocar token anterior si se cambia scope;
- regenerar `token.json` solo dentro del addon;
- verificar que `token.json` sigue ignorado;
- mantener MAIN intacto;
- no crear servicios;
- no crear automatizaciones.

---

## 6. Estado final

```text
PHASE_2_SCOPE_CANDIDATE = gmail.compose
NO_IMPLEMENTATION_YET
NO_OAUTH_CHANGE_YET
NO_SEND_IMPLEMENTED
MAIN_INTACT
```
