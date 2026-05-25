# 🧠 OpenClaw – Estado actual (Checkpoint)

## 🎯 Objetivo

Medir uso real del sistema:
- acciones
- interacciones
- consumo de tokens (estimado)
- calidad de medición

---

## 🏗️ Arquitectura

### Fuente de datos
- logs/resource_usage.jsonl

### Scripts clave
- scripts/ru_event.sh (base)
- scripts/ru_interaction.sh (wrapper con interaction_id automático)
- scripts/export_token_dashboard.py
- scripts/write_daily_log.py

---

## 🔗 Trazabilidad

### Regla operativa

Usar siempre:
```bash
bash scripts/ru_interaction.sh <flow> <action> <target> <result>
