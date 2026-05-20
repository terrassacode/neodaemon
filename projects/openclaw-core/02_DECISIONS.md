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

## D-006 — Cerrar trabajo abierto antes de iniciar nuevas implementaciones

Fecha: 2026-05-20

Estado: aceptado.

Motivo:
Evitar acumulación de piezas a medio cerrar, deriva operativa y falsa sensación de avance.

Regla:
Antes de implementar funcionalidades nuevas, se deben cerrar, validar y documentar las tareas abiertas.

Resultado esperado:
Menos deuda operativa, menos ruido y mayor estabilidad del sistema.

## D-007 — Integrar contexto GitHub mediante snapshot antes de tocar RAG API

Fecha: 2026-05-20

Estado: propuesta aceptada para cierre previo; implementación RAG aplazada.

Motivo:
Evitar acoplar directamente el RAG a múltiples ficheros Markdown o a GitHub en cada petición.

Regla:
Primero crear un snapshot local explícito del contexto. Solo después evaluar integración en RAG API v2.

Resultado esperado:
Contexto controlado, acotado y fácil de auditar antes de cualquier cambio en el servicio RAG.
