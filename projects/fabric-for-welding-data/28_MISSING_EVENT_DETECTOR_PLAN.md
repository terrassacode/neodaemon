# 28_MISSING_EVENT_DETECTOR_PLAN.md

Status: design only  
Scope: detector de acciones relevantes sin evento Resource Usage  
Version: v1.0  
Última actualización: 2026-05-22

---

## 1. Objetivo

Diseñar un detector que identifique posibles cambios o acciones relevantes que no hayan sido registrados mediante:

```bash
/openclaw/workspace/main/scripts/ru_event.sh
```

El objetivo no es automatizar Resource Usage todavía, sino detectar huecos de trazabilidad.

---

## 2. Problema

El sistema actual depende de disciplina manual.

Si MAIN modifica un archivo, valida una acción, crea documentación, toca dashboard o ejecuta una operación relevante sin llamar a `ru_event.sh`, entonces:

- `logs/resource_usage.jsonl` queda incompleto;
- `dashboard-v2/data/resource_usage.json` no refleja toda la actividad;
- `resource_usage_metrics.json` puede infravalorar acciones reales;
- `daily_summary.json` puede construir resúmenes incompletos;
- el dashboard puede parecer más inactivo de lo que realmente estuvo.

---

## 3. Fuentes a comparar

### 3.1 Cambios recientes en archivos

Áreas candidatas:

```text
dashboard-v2/
scripts/
systemd/user/
context_repo/projects/fabric-for-welding-data/
context_repo/projects/fabric/
context_repo/personal/
logs/briefings/
briefings/
daily_reports/
```

Señales posibles:

- `mtime` reciente;
- cambios detectados por Git si el path está trackeado;
- archivos nuevos;
- scripts modificados;
- documentos Markdown creados o actualizados;
- JSON de dashboard actualizado.

### 3.2 Eventos Resource Usage registrados

Fuente primaria actual:

```text
/openclaw/workspace/main/logs/resource_usage.jsonl
```

Campos útiles:

```text
timestamp
flow
action
target
result
```

Fuente exportada:

```text
/openclaw/workspace/main/dashboard-v2/data/resource_usage.json
```

Uso:

- comparar `target` contra archivos cambiados;
- comparar timestamp de evento contra timestamp de modificación;
- identificar acciones con resultado terminal (`ok`, `partial`, `blocked`, `error`).

### 3.3 Log operacional humano actual

Fuente secundaria:

```text
/openclaw/workspace/main/logs/operational_events.log
```

Nota:

- es vista humana auxiliar;
- no debe ser fuente de verdad futura;
- puede ayudar temporalmente a detectar actividad no reflejada en Resource Usage.

### 3.4 Timeline estructurada futura

Fuente de verdad prevista:

```text
/openclaw/workspace/main/logs/operational_timeline.jsonl
```

Cuando exista, el detector debería preferir esta fuente frente a logs humanos.

---

## 4. Criterio de acción relevante

Una acción puede requerir evento Resource Usage si cumple al menos una condición:

- se creó o modificó un archivo relevante;
- se ejecutó una validación significativa;
- se modificó dashboard, scripts, documentación operativa o systemd draft;
- se produjo un resultado terminal: `HECHO`, `HECHO parcial`, `BLOQUEADO`, `ERROR_MODE`;
- se activó/verificó un servicio;
- se creó una alerta o resumen diario;
- se tocó un archivo bajo rutas operativas clave.

No deberían requerir evento:

- lectura pura sin resultado terminal;
- conversación sin acción;
- explicación o análisis sin modificación ni ejecución;
- diagnóstico conceptual sin validación ni cambio de estado.

---

## 5. Algoritmo propuesto

### 5.1 Entrada

Parámetros futuros posibles:

```text
--since "24 hours ago"
--paths dashboard-v2 scripts context_repo/projects/fabric-for-welding-data
--resource-log logs/resource_usage.jsonl
--format text|json
```

### 5.2 Paso 1 — detectar candidatos por archivos

Crear una lista de archivos con modificación reciente.

Ejemplo conceptual:

```text
file_path
mtime
category
```

Categorías:

```text
dashboard
script
documentation
systemd
log_or_data
other
```

### 5.3 Paso 2 — cargar eventos Resource Usage

Leer `logs/resource_usage.jsonl` y normalizar eventos válidos.

Ignorar líneas inválidas.

Campos normalizados:

```text
timestamp
flow
action
target
result
```

### 5.4 Paso 3 — comparar target contra paths

Para cada archivo modificado:

1. buscar evento cuyo `target` coincida exactamente;
2. si no coincide, buscar coincidencia relativa;
3. si no coincide, buscar evento por categoría y ventana temporal;
4. si no hay coincidencia, marcar como `missing_event_candidate`.

### 5.5 Paso 4 — evitar falsos positivos

Excluir o rebajar severidad para:

- archivos de datos generados automáticamente;
- JSON exportados por Resource Usage;
- logs append-only;
- archivos modificados por scripts conocidos;
- archivos temporales o backups;
- cambios antiguos fuera de ventana.

### 5.6 Paso 5 — salida

Salida recomendada en texto:

```text
MISSING_EVENT_CANDIDATES
- path: dashboard-v2/index.html
  reason: modified recently but no ru_event target found
  recommendation: register manual event or mark as accepted exception
```

Salida JSON futura:

```json
{
  "checked_since": "2026-05-22T00:00:00+02:00",
  "candidates": [
    {
      "path": "dashboard-v2/index.html",
      "mtime": "2026-05-22T10:28:00+02:00",
      "category": "dashboard",
      "reason": "modified_recently_without_matching_resource_usage_event",
      "severity": "warning",
      "recommended_event": {
        "flow": "DASHBOARD",
        "action": "dashboard_update",
        "target": "dashboard-v2/index.html",
        "result": "ok"
      }
    }
  ]
}
```

---

## 6. Reglas de seguridad

El detector debe ser read-only.

Permitido:

- leer metadatos de archivos;
- leer logs Resource Usage;
- leer timeline futura;
- imprimir reporte;
- generar salida JSON si se autoriza explícitamente.

No permitido:

- modificar archivos;
- crear eventos automáticamente;
- ejecutar `ru_event.sh` automáticamente;
- tocar runtime;
- tocar servicios;
- tocar RAG;
- leer tokens;
- leer `.env`;
- leer `openclaw.json`;
- hacer commit/push.

---

## 7. Riesgos

### 7.1 Falsos positivos

Puede marcar como faltante un cambio generado automáticamente.

Mitigación:

- allowlist de paths generados;
- categorías de severidad;
- no registrar eventos automáticamente.

### 7.2 Falsos negativos

Puede no detectar acciones sin cambio de archivo.

Ejemplo:

- validación manual ejecutada sin modificar archivos;
- diagnóstico de servicio con resultado importante.

Mitigación:

- comparar también con `operational_timeline.jsonl` cuando exista;
- permitir eventos manuales `VALIDAR_LOW_SCOPE`, `SYSTEMD`, `OTHER`.

### 7.3 Doble conteo

Si el detector genera eventos automáticamente, podría duplicar registros.

Mitigación:

```text
El detector no debe registrar eventos. Solo reportar candidatos.
```

### 7.4 Ruido excesivo

Muchos archivos generados pueden saturar el reporte.

Mitigación:

- agrupar por categoría;
- ocultar data/logs por defecto;
- priorizar dashboard, scripts, systemd y documentación operativa.

---

## 8. Fases de implementación

### Fase 1 — diseño

Estado actual.

Resultado:

```text
Documento de diseño sin implementación.
```

### Fase 2 — detector read-only

Crear script futuro:

```text
/openclaw/workspace/main/scripts/detect_missing_resource_usage_events.py
```

Comportamiento:

- read-only;
- compara mtime/path contra Resource Usage;
- imprime candidatos;
- no escribe logs;
- no ejecuta `ru_event.sh`.

### Fase 3 — reporte manual

Usar el detector para generar propuestas de eventos faltantes.

Ejemplo:

```bash
bash /openclaw/workspace/main/scripts/ru_event.sh DASHBOARD dashboard_update dashboard-v2/index.html ok
```

Solo Albert/MAIN decide si registrar el evento.

### Fase 4 — integración con timeline futura

Cuando exista `operational_timeline.jsonl`, comparar contra esa fuente como autoridad principal.

### Fase 5 — dashboard opcional

Solo si se autoriza más adelante:

- mostrar número de candidatos pendientes;
- no mostrar detalles sensibles;
- no permitir acciones desde dashboard.

---

## 9. Recomendación

Implementar primero como herramienta read-only de diagnóstico.

No automatizar registro de eventos.

No tocar runtime.

No tocar servicios.

No tocar RAG.

Recomendación de próximo paso, si se autoriza:

```text
Crear detect_missing_resource_usage_events.py con salida texto simple y sin escrituras.
```
