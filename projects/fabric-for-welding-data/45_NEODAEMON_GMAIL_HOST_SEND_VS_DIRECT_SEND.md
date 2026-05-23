# 45_NEODAEMON_GMAIL_HOST_SEND_VS_DIRECT_SEND.md

Status: HOST_SEND_WORKING_DIRECT_SEND_PENDING  
Cuenta: `claw.neodaemon@gmail.com`  
Fecha: 2026-05-23  
Addon: `/openclaw/workspace/addons/gmail-readonly`

---

## 1. Resultado

Queda documentada la diferencia operativa actual entre envío desde host y envío directo desde la sesión de Neodaemon.

```text
HOST_GMAIL_SEND = WORKING
NEODAEMON_DIRECT_SEND_TOOL = PENDING
```

---

## 2. Estado real confirmado

Confirmado por prueba desde terminal/host:

```text
gmail_send_check.py funciona
Gmail send funciona desde host
token_send.json operativo
correo real enviado desde claw.neodaemon@gmail.com
```

---

## 3. Limitación actual de Neodaemon

La sesión actual de Neodaemon todavía no dispone de una herramienta activa para enviar email directamente.

Neo puede:

- redactar correos;
- preparar asuntos y cuerpos;
- generar comandos para host;
- documentar hitos;
- usar web_search si está disponible.

Neo no puede todavía:

- invocar Gmail send directamente;
- ejecutar `gmail_send_check.py` por sí mismo;
- usar una tool `gmail_send_controlled`;
- enviar email desde la sesión sin intervención del host.

---

## 4. Flujo operativo actual

Flujo real funcional:

```text
Neo redacta → Albert ejecuta gmail_send_check.py en host → correo enviado
```

Esto permite productividad inmediata sin abrir `exec` general ni crear todavía un plugin custom.

---

## 5. Diferencia importante

No confundir:

```text
host puede enviar = sí
Neo sesión puede enviar directamente = todavía no
```

---

## 6. Próximo paso opcional

Si se quiere eliminar la intervención manual del host, el siguiente trabajo sería crear una acción controlada:

```text
gmail_send_controlled
```

Condiciones mínimas:

- no habilitar `exec` general;
- usar argv fijo o plugin/tool custom;
- usar cuenta dedicada `claw.neodaemon@gmail.com`;
- permitir envío solo bajo confirmación explícita de Albert;
- no permitir envío masivo ni adjuntos automáticos de inicio.

---

## 7. Estado final

```text
HOST_SEND_WORKING
DIRECT_SEND_FROM_NEO_PENDING
NO_EXEC_GENERAL
DEDICATED_ACCOUNT
MAIN_INTACT
```
