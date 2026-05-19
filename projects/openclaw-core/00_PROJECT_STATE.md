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
- dashboard visual
- modelos IA
- análisis OSINT

## Estado actual
- Sistema OpenClaw operativo en VM
- Acceso SSH validado
- Sistema de contexto externo funcionando con GitHub
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

## Restricciones operativas

- No tocar gateway, routing, modelos ni configuración sensible sin permiso explícito.
- No documentar secretos, tokens ni claves reales en este repositorio.
- Si una acción no puede validarse por sandbox, debe marcarse como bloqueo o pendiente de validación externa.

## Siguiente paso
- Definir subcomponentes internos del core: MAIN, TASK_VALIDATOR, gateway, API base, servicios systemd, seguridad, logs y health checks.
