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
- Auditoría host manual realizada por Albert el 2026-05-19: Telegram RAG, RAG API v2, dashboard web y dashboard HTTP aparecen activos; dashboard web escucha en Tailscale por puerto 8090; logs recientes de `telegram-rag.service` sin entradas en las últimas 2 horas.

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
- Sirve por Tailscale en puerto 8090 si se activa desde host.

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

## Matriz operativa inicial

| Componente | Estado | Qué funciona | Qué no funciona / límites | Dudas abiertas | Siguiente acción |
|---|---|---|---|---|---|
| MAIN | Operativo en modo prudente / bootstrap estable | Responde a Albert; mantiene identidad Neodaemon v2; usa memoria operativa; aplica TASK_VALIDATOR; coordina cambios dentro de `/openclaw/workspace/main`; crea/edita documentación, scripts y units preparadas; respeta límites sensibles | No tiene ejecución shell directa en esta sesión; no puede validar `systemctl`, `journalctl` ni comandos host; no puede leer fuera del sandbox si la ruta escapa del workspace autorizado; no puede forzar `sendDocument` por Telegram | Ya se confirmó estado host básico manual; queda definir si MAIN debe tener algún canal de auditoría controlada en el futuro | Mantener ejecución host manual por Albert; no dar shell directo a MAIN todavía |
| Alertas | Timer activo; servicio aparece inactivo/dead entre ejecuciones, coherente con servicio oneshot/dry-run | Timer programado cada ~30 min; checker preparado; lógica ya refinada para reducir ruido | Envío real no confirmado; dry-run/prudente; falta validar salida real de último run y contenido de alerta | Si deben pasar de dry-run a envío real | Revisar último resultado/log de `openclaw-operational-alerts.service` antes de activar envío |
| Telegram | Servicio activo y corriendo; logs sin entradas recientes en últimas 2h | Canal principal disponible; proceso estable desde más de 1 día | No se verificó interacción funcional end-to-end en esta auditoría; no se deben exponer secretos | Confirmar prueba funcional desde Telegram y respuesta RAG | Hacer prueba controlada de mensaje simple y verificar respuesta |
| Dashboard web | Activo y escuchando en puerto 8090 por Tailscale | Servicio web activo; puerto 8090 abierto en IP Tailscale | No se verificó desde navegador externo/móvil en esta auditoría | Confirmar carga real de `status.html` desde cliente Tailscale | Abrir URL desde móvil/cliente Tailscale y comprobar dashboard |

## Restricciones operativas

- No tocar gateway, routing, modelos ni configuración sensible sin permiso explícito.
- No documentar secretos, tokens ni claves reales en este repositorio.
- Si una acción no puede validarse por sandbox, debe marcarse como bloqueo o pendiente de validación externa.

## Siguiente paso
- Validar alertas: revisar último log/resultado del timer y decidir si siguen en dry-run o pasan a envío controlado.
