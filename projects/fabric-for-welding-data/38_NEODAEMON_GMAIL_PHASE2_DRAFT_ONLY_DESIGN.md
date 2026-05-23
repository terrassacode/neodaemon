# 38_NEODAEMON_GMAIL_PHASE2_DRAFT_ONLY_DESIGN.md

Status: PHASE_2_DRAFT_ONLY_DESIGN  
Cuenta: `claw.neodaemon@gmail.com`  
Fecha: 2026-05-23  
Addon: `/openclaw/workspace/addons/gmail-readonly`

---

## 1. Objetivo

Diseñar la Fase 2 de Gmail para Neodaemon: creación y edición de borradores sin envío.

Esta fase todavía no activa nuevos permisos OAuth ni modifica el addon.

---

## 2. Estado de partida

La Fase 1 está validada:

```text
PHASE_1_READONLY_WORKING
GMAIL_API_READONLY = WORKING
scope activo: https://www.googleapis.com/auth/gmail.readonly
```

El addon funciona en entorno aislado y MAIN permanece intacto.

---

## 3. Principio central

```text
Neo puede leer y preparar.
Albert autoriza enviar, borrar o modificar.
```

En Fase 2:

```text
Neo puede preparar borradores.
Neo no puede enviar correos.
```

---

## 4. Capacidades objetivo de Fase 2

Permitido, tras autorización explícita de Albert:

- crear borrador nuevo;
- preparar respuesta a un hilo como borrador;
- editar borrador existente;
- listar borradores para revisión;
- mostrar destinatario, asunto y cuerpo antes de crear o actualizar.

Prohibido:

- enviar correos;
- borrar correos;
- archivar;
- modificar labels;
- descargar adjuntos automáticamente;
- crear reglas automáticas;
- crear borradores sin petición explícita;
- añadir destinatarios inferidos no confirmados.

---

## 5. Riesgo nuevo

La Fase 2 añade riesgo porque requiere permisos superiores a `gmail.readonly`.

Riesgos principales:

- ampliación OAuth demasiado amplia;
- creación de borradores con destinatario incorrecto;
- borradores que contengan secretos;
- confusión entre crear borrador y enviar;
- instrucciones maliciosas dentro de emails intentando provocar respuesta.

---

## 6. Scopes a estudiar

Antes de implementar, hay que verificar el scope mínimo real para borradores.

Candidatos a revisar:

```text
https://www.googleapis.com/auth/gmail.compose
https://www.googleapis.com/auth/gmail.modify
https://mail.google.com/
```

Preferencia de diseño:

```text
usar el scope mínimo que permita crear borradores sin enviar ni modificar buzón más allá de borradores
```

No se debe ampliar a `mail.google.com` salvo que sea técnicamente inevitable y aprobado explícitamente.

---

## 7. Política de confirmación

Antes de crear o actualizar un borrador, Neodaemon debe mostrar:

```text
Cuenta remitente:
Destinatarios:
CC/BCC:
Asunto:
Cuerpo del borrador:
Adjuntos:
Origen de la petición:
Riesgos detectados:
Acción exacta:
```

Albert debe confirmar explícitamente:

```text
CONFIRMO CREAR BORRADOR
```

o:

```text
CONFIRMO ACTUALIZAR BORRADOR
```

Sin confirmación explícita no se crea ni actualiza borrador.

---

## 8. Requisitos técnicos antes de implementar

Antes de tocar código:

- documentar scope elegido;
- revocar y regenerar token si cambia el scope;
- comprobar que `token.json` sigue ignorado;
- comprobar que `client_secret.json` sigue ignorado;
- mantener addon fuera de MAIN;
- no crear servicios;
- no crear automatizaciones;
- no integrar con MAIN todavía.

---

## 9. Validación esperada futura

Una futura implementación de Fase 2 será válida solo si:

- crea un borrador de prueba bajo confirmación;
- no envía ningún correo;
- no modifica labels;
- no borra correos;
- no descarga adjuntos;
- confirma scope activo;
- registra logs sin cuerpo completo ni secretos.

---

## 10. Estado final de este documento

```text
PHASE_2_DRAFT_ONLY_DESIGN
NO_SCOPE_CHANGE_YET
NO_OAUTH_CHANGE_YET
NO_SEND
NO_MODIFY_GENERAL
NO_DELETE
MAIN_INTACT
```
