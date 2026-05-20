# 08_CLOSURE_GUIDE

## Objetivo

Usar esta tabla como guía priorizada para cerrar tareas abiertas antes de iniciar nuevas implementaciones.

Regla principal:

```text
No abrir una fase nueva si la prioridad anterior no está cerrada, validada y documentada.
```

## Tabla de cierre priorizada

| Prioridad | Bloque | Qué hay que cerrar | Estado actual | Criterio de cierre | Siguiente acción |
|---|---|---|---|---|---|
| P1 | Limpieza de salida Ollama | Corregir o mitigar texto repetido, cortado o corrupto en respuestas del RAG | Abierto | Respuesta RAG legible, sin repeticiones evidentes ni cortes tipo palabras duplicadas | Revisar postprocesado actual `clean_answer()` y definir mejora mínima segura |
| P2 | Validación funcional RAG HOT | Confirmar que el RAG responde correctamente usando los 3 chunks curados | Parcialmente validado | Pregunta de prueba devuelve respuesta útil sobre baseline, std_RD, ventana, RobotId y ProgramId | Repetir prueba tras P1 y guardar resultado |
| P3 | Documentación validación RAG | Registrar validación completa de los 3 chunks en GitHub | Parcial | `07_RAG_VALIDATION_LOG.md` actualizado con validación final y limitaciones | Actualizar log cuando P1/P2 estén cerrados |
| P4 | Whitelist de fuentes | Definir fuentes permitidas para búsqueda diaria de Neodaemon | Pendiente | Lista inicial aprobada: Microsoft Learn, GitHub Microsoft y fuentes técnicas concretas | Crear/actualizar sección en `01_SOURCES.md` o archivo específico |
| P5 | Flujo diario Neodaemon → Albert → RAG | Automatizar propuesta diaria de 3 fuentes y curación humana | Diseñado, no implementado | Neodaemon propone 3 fuentes; Albert decide; solo aprobadas generan chunks | Diseñar automatización sin escritura automática en RAG |
| P6 | Generación controlada de chunks | Establecer plantilla y proceso para crear chunks JSON curados | Manual validado | Cada chunk nuevo pasa JSON OK + BM25 OK + registro en GitHub | Crear plantilla de chunk y checklist |
| P7 | Reducción de ruido BM25 | Reducir recuperación secundaria de chunks no relacionados | Detectado | Resultados secundarios no contaminan respuestas o se filtran por source/block_type/quality_score | Evaluar filtro futuro sin tocar API todavía |
| P8 | Baseline con datos reales | Validar el umbral inicial `std_RD_actual > std_RD_baseline * 1.5` con datos reales | Pendiente | Evidencia con datos reales de que el criterio detecta inestabilidad o se ajusta | Pasar a análisis offline, no al RAG |
| P9 | SSD base de conocimiento | Definir si un SSD será base local de conocimiento | Backlog | Alcance, seguridad, estructura, backups y relación GitHub/rag_store definidos | Mantener en backlog hasta cerrar P1-P6 |
| P10 | Token/API hardening | Rotar/externalizar token local de `api_rag_v2.py` | Detectado, no abierto | Token fuera del código y sin exposición en logs/comandos | Tratar como tarea separada de seguridad, no ahora |

## Orden recomendado

```text
P1 -> P2 -> P3 -> P4 -> P5 -> P6
```

No avanzar a P7-P10 hasta cerrar el ciclo básico del RAG curado.

## Estado guía

Creada como referencia principal para evitar desviaciones.
