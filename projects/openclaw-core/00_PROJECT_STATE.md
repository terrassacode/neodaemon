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

## Siguiente paso
- Definir subcomponentes internos del core (API, gateway, servicios)
