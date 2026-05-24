# 39_NEODAEMON_GMAIL_PHASE2_CONTROLLED_SEND_WORKING.md

Status: PHASE_2_CONTROLLED_SEND_WORKING
Estado operativo: WORKING
Cuenta: claw.neodaemon@gmail.com
Addon: /openclaw/workspace/addons/gmail-readonly
Plugin: gmail-send-plugin
Tool: gmail_send_controlled
Fecha: 2026-05-23

## Resultado

Neodaemon ya puede enviar emails reales mediante una herramienta controlada.

Resultado validado:

STATUS=OK
ACTION=gmail_send_controlled
MESSAGE_ID=19e5a20e14399046

Esto confirma que la Fase 2 controlled-send está operativa.

## Arquitectura validada

OpenClaw MAIN
-> gmail_send_controlled
-> gmail-send-plugin
-> Gmail API
-> claw.neodaemon@gmail.com

La integración se mantiene como addon/plugin separado.

## Estado final validado

GMAIL_PHASE_2_CONTROLLED_SEND = WORKING
PLUGIN_STATUS = loaded
TOOL_VISIBLE_IN_MAIN = yes
TOOL_OPTIONAL = true
SEND_TEST = OK

## Problemas encontrados

1. OpenClaw bloqueó child_process.
2. Faltaba openclaw.plugin.json.
3. Faltaba configSchema.
4. El registro del plugin debía ser síncrono.
5. La tool debía registrarse como optional.
6. MAIN no veía la tool hasta añadirla a allowlist.
7. Gmail API devolvía invalid_request.

## Correcciones aplicadas

MIME correcto:

const message = `To: ${to}
Content-Type: text/plain; charset=utf-8
MIME-Version: 1.0
Subject: ${subject}

${body}`;

Encoding base64url correcto:

const encodedMessage = Buffer.from(message)
  .toString("base64")
  .replace(/\+/g, "-")
  .replace(/\//g, "_")
  .replace(/=+$/, "");

OAuth2 adaptado al token generado:

const auth = new google.auth.OAuth2(
  token.client_id,
  token.client_secret
);

auth.setCredentials({
  access_token: token.token,
  refresh_token: token.refresh_token,
  expiry_date: token.expiry ? Date.parse(token.expiry) : undefined
});

Envío Gmail API correcto:

const res = await gmail.users.messages.send({
  userId: "me",
  requestBody: {
    raw: encodedMessage
  }
});

## Seguridad mantenida

NO exec general
NO child_process
NO bash
NO shell libre
NO envío automático
NO borrado de correos
NO modificación de labels
NO uso de Gmail como memoria operativa

## Riesgos pendientes

RISK_LEVEL = medium

Motivos:
- ya existe capacidad real de envío externo;
- depende de token local;
- requiere disciplina de uso;
- conviene añadir logging mínimo y política de destinatarios.

## Próximos pasos recomendados

1. Documentar ubicación del plugin y archivos locales.
2. Añadir logging mínimo sin cuerpo completo del mensaje.
3. Añadir allowlist opcional de destinatarios.
4. Añadir validación de destinatario único.
5. Revisar si requireApproval nativo está activo en flujo real.
6. Crear runbook de rollback.

## Estado final

PHASE_2_CONTROLLED_SEND_WORKING
GMAIL_SEND_CONTROLLED_OK
MESSAGE_ID_CONFIRMED
MAIN_CAN_USE_TOOL
CORE_NOT_MODIFIED
