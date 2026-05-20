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
