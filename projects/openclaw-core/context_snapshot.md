=== PROJECT STATE ===
# 00_PROJECT_STATE

## Update 2026-05-20
- Alertas operativas activadas en modo real (--send)
- RAG estabilizado tras control de BrokenPipeError
- Validación end-to-end completada (Telegram ↔ RAG ↔ MAIN)
- Sistema en estado estable y limpio

---

## Proyecto
openclaw-core

## Objetivo
Gestionar el núcleo del sistema OpenClaw: despliegue, servicios base y arquitectura principal.

## Estado operativo actual
- Telegram: OK
- RAG API v2: OK
- Alertas: activas y calibradas
- Briefing diario: activo

## Notas
- Alertas solo envían cuando ALERT=true
- Ventana temporal de 2h puede arrastrar eventos antiguos
- No se almacenan secretos en este repo

=== DECISIONS ===
# 02_DECISIONS

## D-001
Separar OpenClaw core del sistema de contexto ChatGPT.

Motivo:
Evitar mezclar código sensible con contexto de IA.

## D-002 — Estabilizar RAG API v2

Fecha: 2026-05-20

Estado: aplicado y validado.

Motivo:
Reducir ruido operativo en logs y evitar falsos positivos en alertas.

Resultado:
RAG API v2 queda estable y validado con prueba end-to-end.

## D-003 — Activar alertas operativas reales

Fecha: 2026-05-20

Estado: aplicado y validado.

Motivo:
Pasar de monitorización pasiva a sistema proactivo.

Resultado:
Las alertas se ejecutan automáticamente y solo notifican cuando hay señal real.

## D-004 — Mantener control humano en host

Fecha: 2026-05-20

Estado: aceptado.

Motivo:
Mantener seguridad operativa.

Modelo:
- Albert ejecuta acciones en host.
- Neodaemon propone, valida y documenta.

## D-005 — Usar GitHub como memoria externa

Fecha: 2026-05-20

Estado: aceptado.

Motivo:
Evitar dependencia de chats largos.

Resultado:
GitHub guarda estado, decisiones y handoff prompts.

=== HANDOFF ===
# 99_HANDOFF_PROMPT

## Contexto

Sistema OpenClaw desplegado en VM.

Separación de roles:
- ChatGPT: razonamiento
- GitHub: memoria
- OpenClaw: ejecución

## Estado actual

- RAG API v2 estable
- Telegram validado
- Alertas automáticas activas (--send)
- Briefing diario activo

Sistema sin errores activos.

## Flujo

Albert → Neodaemon → validación → ejecución → respuesta

## Reglas

- Neodaemon no ejecuta en host
- Albert ejecuta en host
- Validación previa obligatoria

## Prioridad

1. Alertas
2. MAIN
3. Telegram

## Objetivo

Sistema autónomo supervisado con control humano.
