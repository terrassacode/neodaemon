# 12_RAG_OPS_WRAPPER_SAFETY_RULES

## Objetivo

Reordenar la implementación de `rag_ops_guarded` para que Neodaemon pueda usar wrappers seguros sin convertirse en un ejecutor libre del host.

---

## Regla principal

```text
Primero seguridad y lectura.
Después validación.
Después acciones controladas.
Después escritura.
```

No se implementan scripts de reinicio, consulta con token o escritura hasta cerrar la fase de lectura.

---

## Fases reordenadas

| Fase | Nombre | Qué permite | Qué NO permite | Estado |
|---|---|---|---|---|
| F0 | Reglas de seguridad | Definir permisos, logs, formato y límites | Ejecutar scripts reales | definido |
| F1 | Lectura pura | Estado servicio, logs, conteo chunks | Reinicios, tokens, escritura, `/rag-ask` | siguiente |
| F2 | Validación local | `py_compile`, `json.tool`, BM25 sin Ollama | Reinicio, token, escritura | pendiente |
| F3 | Acciones autorizadas | Reinicio RAG y consulta local con token oculto | Escritura automática | pendiente |
| F4 | Escritura controlada | Crear chunks/parches con backup | Cambios sin TASK_VALIDATOR | futura |

---

## Scripts permitidos por fase

### F1 — Lectura pura

| Script | Propósito | Riesgo |
|---|---|---|
| `rag_status_readonly.sh` | Ver estado y logs del servicio RAG | bajo |
| `rag_count_chunks.sh` | Contar y listar nombres de chunks JSON | bajo |

### F2 — Validación local

| Script | Propósito | Riesgo |
|---|---|---|
| `rag_py_compile.sh` | Validar sintaxis de `/openclaw/api_rag_v2.py` | bajo |
| `rag_validate_chunk_json.sh` | Validar JSON de un chunk | bajo |
| `rag_test_bm25.sh` | Probar recuperación BM25 sin Ollama ni token | bajo-medio |
| `rag_test_clean_answer.sh` | Probar limpieza de texto con casos artificiales | bajo-medio |

### F3 — Acciones autorizadas

| Script | Propósito | Requiere OK |
|---|---|---|
| `rag_restart_authorized.sh` | Reiniciar `openclaw-rag-v2.service` | sí |
| `rag_query_local.sh` | Consultar `/rag-ask` leyendo token sin imprimirlo | sí |

### F4 — Escritura controlada

| Script | Propósito | Requiere OK |
|---|---|---|
| `rag_create_chunk_guarded.sh` | Crear chunk con validación y backup si aplica | sí |
| `rag_patch_api_guarded.sh` | Aplicar parche autorizado a `api_rag_v2.py` | sí |

F4 no se implementa todavía.

---

## Reglas obligatorias para todos los scripts

1. Usar rutas fijas.
2. No aceptar comandos arbitrarios.
3. Validar argumentos.
4. No imprimir tokens.
5. No usar `sudo`.
6. No instalar paquetes.
7. No acceder a internet.
8. Usar `set -euo pipefail`.
9. Usar `timeout` cuando aplique.
10. Devolver salida estructurada.

---

## Formato de salida estándar

Cada script debe imprimir como mínimo:

```text
STATUS=OK|ERROR|BLOCKED
SCRIPT=<nombre>
MODE=readonly|validation|authorized|write
RESULT=<resumen>
NEXT=<siguiente acción recomendada>
```

Si hay error:

```text
ERROR=<mensaje breve>
```

---

## Logs

Los wrappers deben registrar ejecución en:

```text
/openclaw/workspace/main/logs/rag_ops/
```

Formato recomendado:

```text
YYYY-MM-DD_HHMMSS_<script>.log
```

No registrar tokens ni secretos.

---

## Permisos recomendados

Directorio:

```bash
chmod 750 /openclaw/workspace/main/scripts/rag_ops
```

Scripts:

```bash
chmod 750 /openclaw/workspace/main/scripts/rag_ops/*.sh
```

Propietario esperado:

```text
openclaw
```

---

## Prohibiciones explícitas

```text
No sudo.
No rm -rf.
No editar tokens.
No editar gateway.
No editar Telegram.
No tocar systemd units salvo autorización especial.
No reiniciar servicios fuera de openclaw-rag-v2.service.
No ejecutar curl externo.
No escribir fuera de rutas permitidas.
```

---

## Orden inmediato de implementación

Crear solo estos dos scripts:

```text
1. rag_status_readonly.sh
2. rag_count_chunks.sh
```

Después probarlos manualmente desde host.

Solo si funcionan bien se pasa a F2.

---

## Criterio de cierre F1

F1 se cierra cuando:

1. Existe `/openclaw/workspace/main/scripts/rag_ops/`.
2. Existen `rag_status_readonly.sh` y `rag_count_chunks.sh`.
3. Ambos scripts ejecutan sin modificar el sistema.
4. Ambos devuelven salida estructurada.
5. Ambos generan log sin secretos.
6. Albert confirma que reducen copia/pega operativo.

---

## Estado

Reordenado.
Siguiente paso: implementar F1 con dos scripts read-only.
