# 00_PROJECT_STATE

## Proyecto
openclaw-core

## Objetivo
Gestionar el núcleo del sistema OpenClaw: despliegue, servicios base y arquitectura principal.

## Alcance del core

### Incluye
- arranque del sistema
- servicios systemd
- gateway
- API base
- estructura de carpetas
- seguridad operativa
- logs básicos
- health checks
- flujo MAIN de control operativo

### NO incluye
- RAG avanzado
- Telegram bot
- dashboard visual avanzado
- modelos IA
- análisis OSINT

## Estado actual
- Sistema OpenClaw operativo en VM.
- Acceso SSH validado.
- Sistema de contexto externo funcionando con GitHub.
- Telegram/RAG no está bloqueado por la antigua hipótesis de botToken; se usa otro sistema de autenticación que no debe documentarse aquí con secretos.

## Flujo operativo principal

```text
Albert -> Neodaemon/MAIN -> validación -> ejecución/consulta -> verificación -> respuesta a Albert
```

## Pasos del flujo

1. Albert envía una petición por Telegram, webchat o TUI.
2. Neodaemon/MAIN interpreta si es respuesta simple, lectura, escritura, ejecución, sistema, red o acción sensible.
3. TASK_VALIDATOR evalúa acción, tipo, riesgo, rutas afectadas, operación, rollback y validación.
4. Si requiere autorización, Albert debe autorizar explícitamente antes de ejecutar.
5. Neodaemon ejecuta solo dentro del alcance autorizado.
6. Neodaemon valida resultado: archivo, contenido, ruta, logs o estado esperado.
7. Neodaemon responde con lo hecho, lo validado, lo pendiente y los bloqueos.
8. Si hay subagentes, MAIN mantiene control y síntesis final.

## Subcomponentes reales actuales

### Albert
- Origen de órdenes, autorizaciones y decisiones finales.

### Neodaemon/MAIN
- Agente principal.
- Interpreta, coordina, valida, ejecuta dentro de límites y responde.

### TASK_VALIDATOR
- Capa/protocolo de evaluación de riesgo.
- Genera veredicto humano y JSON antes de actuar.
- Decide si se puede ejecutar, pedir autorización o bloquear.

### Workspace
- Ruta principal: `/openclaw/workspace/main`.
- Zona principal para documentación, scripts, dashboards y unidades preparadas.

### Memoria operativa local
- `MEMORY.md`
- `AGENTS.md`
- `SOUL.md`
- `USER.md`
- Guardan identidad, reglas, preferencias y estado operativo.

### Sistema de briefings
- `scripts/generate_daily_briefing.sh`
- `briefings/YYYY/MM/DD/briefing.md`
- `briefingDD_MM_YYYY.pdf`
- Logs en `logs/briefings/...`.

### Sistema de alertas
- `scripts/check_operational_alerts.sh`
- `alerts/alert.txt`
- Units preparadas:
  - `openclaw-operational-alerts.service`
  - `openclaw-operational-alerts.timer`

### Dashboard CLI
- `scripts/status_dashboard.sh`

### Dashboard HTML
- `dashboard/status.html`
- `scripts/generate_status_dashboard_html.sh`
- Units preparadas:
  - `openclaw-dashboard-html.service`
  - `openclaw-dashboard-html.timer`

### Dashboard web local preparado
- `openclaw-dashboard-web.service`
- Sirve por Tailscale en `100.117.135.114:8090` si se activa desde host.

### Telegram/RAG externos
- `telegram-rag.service`
- `openclaw-rag-v2.service`
- Monitorización parcial mediante logs/alertas.
- No se deben tocar sin autorización explícita.

### Systemd user
- Capa de automatización preparada o activada desde host.
- Neodaemon prepara units; la activación real queda controlada.

### Herramientas disponibles en esta sesión
- Lectura/escritura de archivos.
- Patches.
- Memoria.
- Sin ejecución shell directa ahora mismo.

## Prioridad operativa actual

1. MAIN
   - Cerebro operativo del sistema.
   - Sin MAIN no hay coordinación, memoria operativa, validación, síntesis ni control de seguridad.

2. Alertas
   - Primera capa de vigilancia operativa.
   - Detectan señales de fallo antes de que Albert tenga que revisar logs manualmente.
   - Están en fase prudente, dry-run o refinamiento.

3. Telegram
   - Canal humano principal.
   - Debe servir para interacción, alertas y briefings.
   - Queda por debajo de MAIN y Alertas porque sin cerebro operativo ni vigilancia calibrada Telegram sería solo transporte.

Resumen conceptual:

```text
MAIN = cerebro operativo
Alertas = sistema nervioso
Telegram = canal de comunicación
```

## Restricciones operativas

- No tocar gateway, routing, modelos ni configuración sensible sin permiso explícito.
- No documentar secretos, tokens ni claves reales en este repositorio.
- Si una acción no puede validarse por sandbox, debe marcarse como bloqueo o pendiente de validación externa.

## Siguiente paso
- Convertir la prioridad operativa en una matriz: componente, estado, criticidad, validación y siguiente acción.
