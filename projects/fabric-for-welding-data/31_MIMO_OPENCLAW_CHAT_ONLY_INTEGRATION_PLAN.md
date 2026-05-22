# 31_MIMO_OPENCLAW_CHAT_ONLY_INTEGRATION_PLAN.md

Status: design only  
Scope: MiMo como agente OpenClaw separado `mimo-chat-only`  
Modelo objetivo: `xiaomi/mimo-v2-flash`  
Última actualización: 2026-05-22

---

## 1. Objetivo

Diseñar una integración futura de Xiaomi MiMo dentro de OpenClaw como agente separado, exclusivamente conversacional.

La integración debe permitir pruebas controladas de MiMo sin afectar a Neodaemon/MAIN.

Este documento no autoriza activación.

---

## 2. Principio principal

Neodaemon/MAIN no cambia.

```text
Albert → Neodaemon/MAIN → subagentes → Neodaemon/MAIN → Albert
```

MiMo queda fuera del flujo operativo MAIN.

MiMo no coordina, no valida, no ejecuta y no decide.

---

## 3. Estado objetivo

Agente documental propuesto:

```text
mimo-chat-only
```

Estado:

```text
chat_only / friendly_companion
```

Modelo objetivo:

```text
xiaomi/mimo-v2-flash
```

Provider objetivo:

```text
xiaomi
```

---

## 4. Reglas obligatorias

MiMo/OpenClaw chat_only:

- no es primary;
- no es fallback;
- no participa en routing automático;
- no sustituye a MAIN;
- no usa tools;
- no usa RAG;
- no usa filesystem;
- no toca runtime;
- no recibe secretos;
- no accede a tokens;
- no lee logs privados;
- no toma decisiones técnicas;
- no valida acciones MAIN;
- no ejecuta comandos;
- no modifica archivos;
- no toca servicios;
- no toca gateway;
- no toca configuración sensible.

---

## 5. Uso permitido

Permitido solo:

- conversación informal;
- compañía;
- ideas ligeras;
- creatividad no crítica;
- conversación general sin impacto operativo;
- reformulación no sensible;
- entretenimiento.

Si el usuario pide algo operativo, MiMo debe responder:

```text
Esto debe hacerlo Neodaemon/MAIN.
```

---

## 6. Telegram separado

MiMo debe usar un canal Telegram separado del canal de Neodaemon/MAIN.

Reglas:

- bot/token separado;
- sesión separada;
- identidad separada;
- sin routing automático desde MAIN;
- sin compartir contexto MAIN;
- sin acceso a memoria privada de Neodaemon;
- sin acceso a RAG;
- sin tools.

Objetivo:

```text
Evitar confusión entre chat amistoso MiMo y operación real MAIN.
```

---

## 7. Validaciones requeridas antes de activar

Antes de cualquier cambio de configuración real, validar manualmente en host:

### 7.1 Provider disponible

Comando pendiente:

```bash
openclaw models list --provider xiaomi
```

Criterio:

```text
El provider xiaomi aparece disponible sin errores.
```

### 7.2 Modelo disponible

Dentro de la salida debe aparecer:

```text
xiaomi/mimo-v2-flash
```

Criterio:

```text
El modelo objetivo existe y es seleccionable.
```

### 7.3 Agente definido documentalmente

Antes de activar cualquier agente real, debe existir documentación final de:

- nombre del agente;
- modelo;
- canal Telegram separado;
- límites chat_only;
- no tools;
- no RAG;
- no filesystem;
- no runtime;
- no secretos;
- respuesta obligatoria ante peticiones operativas.

Este documento cumple la definición preliminar, no la activación.

---

## 8. Configuración futura propuesta, no activa

Borrador conceptual, no aplicar todavía:

```yaml
agent: mimo-chat-only
model: xiaomi/mimo-v2-flash
mode: chat_only
tools: []
rag: disabled
filesystem: disabled
runtime: disabled
routing: manual_only
fallback: false
primary: false
telegram: separated
```

Este bloque es solo diseño. No debe copiarse a configuración real sin revisión.

---

## 9. Riesgos

### 9.1 Confusión de identidad

Riesgo: que el usuario trate a MiMo como si fuera Neodaemon.

Mitigación:

- nombre separado;
- Telegram separado;
- respuesta fija para tareas operativas;
- sin acceso a contexto MAIN.

### 9.2 Fuga de datos sensibles

Riesgo: enviar secretos o contexto privado a un modelo experimental.

Mitigación:

- no secretos;
- no tokens;
- no memoria;
- no logs;
- no RAG;
- no datos industriales.

### 9.3 Routing accidental

Riesgo: MiMo actúe como fallback o reciba tráfico operativo.

Mitigación:

- no primary;
- no fallback;
- no routing automático;
- activación solo manual y explícita.

### 9.4 Alucinación

Riesgo: MiMo responda como si pudiera operar el sistema.

Mitigación:

- prompt chat_only;
- sin herramientas;
- sin filesystem;
- respuesta obligatoria: `Esto debe hacerlo Neodaemon/MAIN.`

---

## 10. Secuencia segura futura

Si Albert autoriza avanzar:

1. validar provider:
   ```bash
   openclaw models list --provider xiaomi
   ```
2. confirmar modelo:
   ```text
   xiaomi/mimo-v2-flash
   ```
3. preparar propuesta de agente `mimo-chat-only`;
4. revisar riesgos;
5. pedir confirmación explícita;
6. aplicar cambio mínimo de configuración;
7. validar que MAIN no cambia;
8. validar que MiMo no tiene tools/RAG/filesystem/runtime;
9. probar Telegram separado con texto no sensible;
10. documentar resultado.

---

## 11. Estado actual

```text
DISEÑADO DOCUMENTALMENTE
NO CONFIGURADO
NO ACTIVADO
NO GATEWAY
NO ROUTING
NO PRIMARY
NO FALLBACK
NO TOOLS
NO RAG
NO FILESYSTEM
NO RUNTIME
NO SECRETOS
NO COMMIT/PUSH
```

Validación real pendiente por falta de ejecución shell en esta sesión:

```bash
openclaw models list --provider xiaomi
```
