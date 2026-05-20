# 09_PRE_P2_NEODAEMON_SKILL_PLAN

## Objetivo

Crear un plan previo a P2 para cambiar el modo de trabajo actual.

Situación actual:

```text
ChatGPT piensa -> Albert copia/pega -> Neodaemon ejecuta -> Albert devuelve resultado
```

Objetivo nuevo:

```text
ChatGPT diseña estrategia general -> Neodaemon ejecuta pasos operativos guiados -> Albert autoriza decisiones críticas
```

Albert no debe ser solo el intermediario de copia/pega.

---

## Principio de diseño

Neodaemon debe convertirse en ejecutor operativo con skill propia, pero sin perder control humano.

Roles:

| Rol | Responsabilidad |
|---|---|
| ChatGPT | Cabeza pensante, diseño de estrategia, revisión crítica, decisiones de arquitectura |
| Neodaemon | Ejecución operativa paso a paso, validación local, lectura/escritura controlada, logs |
| Albert | Autorización, curación, criterio industrial, aprobación de riesgo |
| GitHub | Memoria externa, decisiones, estado y handoff |
| RAG local | Contexto técnico curado para respuestas y recuperación |

---

## Regla de oro

```text
Neodaemon puede ejecutar tareas repetibles y validadas.
Albert debe autorizar acciones de riesgo medio/alto.
ChatGPT no debe convertirse en operador de comandos manuales.
```

---

## Qué debe hacer la skill de Neodaemon

La skill debe conocer y ejecutar flujos estándar para:

1. Crear backups antes de modificar archivos.
2. Aplicar parches mínimos sobre archivos autorizados.
3. Validar sintaxis con `py_compile` o JSON tool.
4. Ejecutar pruebas artificiales.
5. Reiniciar servicios solo con autorización.
6. Consultar status y journalctl.
7. Registrar resultado.
8. Proponer rollback si algo falla.
9. Actualizar GitHub/context_repo cuando corresponda.
10. No tocar tokens, gateway, Telegram o servicios no relacionados sin autorización explícita.

---

## Límites de la skill

Neodaemon NO debe:

- modificar `api_rag_v2.py` sin TASK_VALIDATOR;
- reiniciar servicios sin autorización;
- escribir chunks RAG sin validación;
- hacer scraping o navegación sin permiso;
- guardar contenido bruto sin curación;
- tocar tokens o configuración sensible;
- mezclar OpenClaw-core con fabric-for-welding-data;
- saltar de prioridad sin cerrar la anterior.

---

## Flujo operativo propuesto

### 1. ChatGPT define intención

Ejemplo:

```text
Cerrar P2: validar que el RAG HOT responde correctamente con los tres chunks curados.
```

### 2. Neodaemon prepara TASK_VALIDATOR

Debe devolver:

- acción;
- tipo;
- riesgo;
- rutas afectadas;
- comandos previstos;
- rollback;
- validación;
- safe_to_execute.

### 3. Albert autoriza o rechaza

Regla:

```text
Sin OK explícito no hay escritura ni reinicio.
```

### 4. Neodaemon ejecuta

Debe ejecutar solo lo autorizado.

### 5. Neodaemon devuelve resultado estructurado

Formato mínimo:

```text
HECHO / BLOQUEADO / ERROR
Archivos tocados:
Backups:
Validación:
Servicios:
Errores:
Siguiente acción recomendada:
```

### 6. ChatGPT revisa críticamente

ChatGPT decide si:

- se cierra la prioridad;
- se repite prueba;
- se hace rollback;
- se documenta en GitHub;
- se pasa a la siguiente prioridad.

---

## Skill mínima inicial: `rag_ops_guarded`

### Propósito

Skill para operaciones controladas sobre el RAG local de OpenClaw.

### Capacidades iniciales

| Comando lógico | Descripción |
|---|---|
| `inspect_rag_api` | Inspecciona funciones relevantes sin modificar |
| `patch_api_prompt` | Modifica solo prompt autorizado |
| `patch_clean_answer` | Modifica solo limpieza de respuesta autorizada |
| `validate_py` | Ejecuta `python3 -m py_compile` |
| `test_clean_answer` | Ejecuta prueba artificial de limpieza |
| `restart_rag_service` | Reinicia `openclaw-rag-v2.service` si está autorizado |
| `test_rag_query` | Lanza consulta controlada a `/rag-ask` sin exponer token |
| `validate_chunk_json` | Valida JSON de chunk |
| `test_bm25` | Prueba recuperación BM25 sin Ollama |
| `write_validation_log` | Prepara actualización documental |

---

## Plantilla de instrucción para Neodaemon

```text
/main Neodaemon, usa la skill rag_ops_guarded.

Objetivo:
[describir objetivo]

Modo:
- primero inspección;
- luego TASK_VALIDATOR;
- no ejecutar escritura sin autorización;
- no reiniciar servicios sin autorización;
- registrar rollback y validación.

Restricciones:
- no tocar tokens;
- no tocar gateway;
- no tocar Telegram;
- no tocar archivos fuera del objetivo;
- no mezclar proyectos.

Salida requerida:
HECHO / BLOQUEADO / ERROR
Riesgo
Archivos afectados
Comandos ejecutados
Validación
Rollback
Siguiente paso
```

---

## Aplicación inmediata antes de P2

Antes de iniciar P2, hay que cerrar esta preparación:

| Paso | Acción | Estado |
|---|---|---|
| preP2-1 | Crear este plan | hecho |
| preP2-2 | Definir skill mínima `rag_ops_guarded` | pendiente |
| preP2-3 | Crear prompt operativo para Neodaemon | pendiente |
| preP2-4 | Probar la skill con tarea de solo lectura | pendiente |
| preP2-5 | Usar la skill para P2 | pendiente |

---

## Criterio de cierre preP2

preP2 se considera cerrado cuando exista:

1. Plan documentado.
2. Skill mínima definida.
3. Prompt operativo listo.
4. Primer uso de prueba en modo solo lectura.
5. Confirmación de que Albert ya no actúa como simple copia/pega operativo.

---

## Siguiente paso recomendado

Crear el documento de la skill:

```text
10_SKILL_RAG_OPS_GUARDED.md
```

Ese archivo debe definir exactamente cómo debe comportarse Neodaemon al ejecutar operaciones RAG controladas.
