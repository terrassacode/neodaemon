# 🧠 HANDOFF PROMPT – OpenClaw Token System

Quiero que actúes como experto en OpenClaw y sistemas de trazabilidad de uso.

## Contexto del sistema

Estoy trabajando en un entorno OpenClaw (Neodaemon) donde he construido un sistema para medir:

- acciones ejecutadas
- interacciones (preguntas)
- consumo de tokens (estimado)
- calidad de medición

---

## Arquitectura actual

Fuente de datos:
- logs/resource_usage.jsonl

Scripts clave:
- scripts/ru_event.sh (base)
- scripts/ru_interaction.sh (wrapper con interaction_id automático)
- scripts/export_token_dashboard.py
- scripts/write_daily_log.py

---

## Regla crítica

Todo evento funcional debe tener interaction_id.

Uso obligatorio:

```bash
bash scripts/ru_interaction.sh <flow> <action> <target> <result>
