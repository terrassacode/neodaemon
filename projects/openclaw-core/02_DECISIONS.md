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
