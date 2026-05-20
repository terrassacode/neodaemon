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
