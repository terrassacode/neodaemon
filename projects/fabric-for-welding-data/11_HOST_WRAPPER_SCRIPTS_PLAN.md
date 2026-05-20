# 11_HOST_WRAPPER_SCRIPTS_PLAN

## Decisión

Opción elegida: B — crear wrapper scripts seguros.

Objetivo:

```text
Reducir el papel de Albert como copia/pega operativo sin dar a Neodaemon acceso libre al host.
```

---

## Principio

Neodaemon no debe ejecutar comandos arbitrarios.

Debe invocar scripts pequeños, revisables y con funciones cerradas.

```text
Skill limitada + scripts seguros + autorización humana = ejecución controlada
```

---

## Ubicación propuesta

```text
/openclaw/workspace/main/scripts/rag_ops/
```

Todos los scripts deben estar dentro del workspace para que sean versionables, revisables y auditables.

---

## Scripts propuestos

| Script | Modo | Propósito | Riesgo |
|---|---|---|---|
| `rag_status_readonly.sh` | lectura | Ver estado de `openclaw-rag-v2.service` y últimos logs | bajo |
| `rag_count_chunks.sh` | lectura | Contar chunks JSON en `rag_store/chunks_v2` | bajo |
| `rag_validate_chunk_json.sh` | lectura/validación | Validar un chunk JSON concreto con `python3 -m json.tool` | bajo |
| `rag_test_bm25.sh` | lectura/test | Ejecutar prueba BM25 sin Ollama | bajo-medio |
| `rag_test_clean_answer.sh` | lectura/test | Probar `clean_answer()` con texto artificial | bajo-medio |
| `rag_py_compile.sh` | validación | Ejecutar `python3 -m py_compile /openclaw/api_rag_v2.py` | bajo |
| `rag_restart_authorized.sh` | sistema | Reiniciar `openclaw-rag-v2.service` solo tras autorización | medio |
| `rag_query_local.sh` | test | Consultar `/rag-ask` sin exponer token | medio |

---

## Regla de seguridad

Los scripts deben:

- usar rutas fijas;
- no aceptar comandos arbitrarios;
- validar argumentos;
- no imprimir tokens;
- no usar `sudo`;
- no modificar archivos salvo scripts específicamente diseñados para ello;
- devolver salida estructurada;
- fallar de forma segura.

---

## Scripts de lectura iniciales

### 1. `rag_status_readonly.sh`

Debe ejecutar solo:

```bash
systemctl --user status openclaw-rag-v2.service --no-pager
journalctl --user -u openclaw-rag-v2.service -n 80 --no-pager
```

No reinicia nada.

---

### 2. `rag_count_chunks.sh`

Debe ejecutar:

```bash
find /openclaw/workspace/main/rag_store/chunks_v2 -maxdepth 1 -type f -name '*.json' | wc -l
```

Opcionalmente listar nombres, no contenido completo.

---

### 3. `rag_py_compile.sh`

Debe ejecutar:

```bash
python3 -m py_compile /openclaw/api_rag_v2.py
```

No modifica archivos.

---

### 4. `rag_test_bm25.sh`

Debe aceptar una query de texto como argumento y ejecutar recuperación BM25 sin pasar por Ollama.

Debe mostrar:

- score;
- chunk_id;
- url;
- título si existe.

No debe llamar a `/rag-ask`.

---

## Scripts que requieren autorización explícita

### `rag_restart_authorized.sh`

Solo debe reiniciar:

```bash
systemctl --user restart openclaw-rag-v2.service
```

Debe ejecutarse solo después de OK explícito de Albert.

---

### `rag_query_local.sh`

Debe consultar `/rag-ask` leyendo el token localmente sin imprimirlo.

Debe evitar exponer el token en salida.

Ejemplo conceptual:

```bash
TOKEN=$(grep -oP 'API_TOKEN\s*=\s*"\K[^"]+' /openclaw/api_rag_v2.py)
curl --max-time 300 -sS "http://127.0.0.1:5001/rag-ask?q=<query_encoded>&token=$TOKEN"
```

Debe usarse solo con autorización porque usa token local.

---

## Lo que NO deben hacer estos scripts

```text
No editar api_rag_v2.py.
No crear chunks.
No borrar chunks.
No modificar systemd units.
No tocar Telegram.
No tocar gateway.
No tocar tokens.
No instalar paquetes.
No acceder a internet.
```

Los scripts de escritura se diseñarán después, si hacen falta.

---

## Fase 1 recomendada

Crear solo scripts de lectura:

```text
rag_status_readonly.sh
rag_count_chunks.sh
rag_py_compile.sh
rag_test_bm25.sh
```

Validar que Albert puede ejecutarlos y que Neodaemon puede invocarlos si obtiene acceso limitado.

---

## Fase 2 recomendada

Crear scripts con autorización:

```text
rag_restart_authorized.sh
rag_query_local.sh
```

Solo después de validar Fase 1.

---

## Criterio de cierre

Esta fase se considera cerrada cuando:

1. Existen scripts de lectura seguros.
2. Se han probado manualmente desde host.
3. No imprimen secretos.
4. No modifican estado del sistema.
5. Neodaemon puede usarlos como interfaz en lugar de comandos libres.

---

## Estado

Plan creado.
Pendiente: implementar Fase 1.
