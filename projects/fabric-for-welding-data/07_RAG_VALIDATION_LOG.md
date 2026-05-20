# 07_RAG_VALIDATION_LOG

## 2026-05-20 — Primera validación de chunk curado

### Objetivo

Comprobar si el RAG local de OpenClaw recupera un nuevo chunk JSON añadido manualmente a:

```text
/openclaw/workspace/main/rag_store/chunks_v2
```

### Chunk probado

```text
fabric_rti_operations_accelerator_001.json
```

Fuente:

```text
Microsoft Real-Time Intelligence Operations Solution Accelerator
```

### Resultado técnico inicial

El endpoint `/rag-ask` respondió con HTTP 200 y devolvió respuesta JSON.

El primer resultado recuperado fue el chunk nuevo:

```text
chunk_id: fabric_rti_operations_accelerator_001
score: 10.04 aprox.
```

### Ajuste posterior

El chunk fue actualizado para reforzar terminología específica de soldadura:

- RD
- variabilidad RD
- robot
- programa
- corriente
- esfuerzo
- soldadura individual como evento
- modelo HOT
- Eventstream
- Eventhouse
- KQL
- alertas/dashboard

### Validación BM25 posterior

Consulta de recuperación directa, sin pasar por Ollama:

```text
RD soldadura robot programa variabilidad Eventstream Eventhouse KQL
```

Resultado:

```text
chunk_id: fabric_rti_operations_accelerator_001
score: 29.05 aprox.
```

El chunk nuevo queda claramente como primer resultado.

### Conclusión

El RAG actual sí consume nuevos archivos JSON añadidos a `rag_store/chunks_v2` sin necesidad de modificar `api_rag_v2.py` ni reiniciar servicios.

La recuperación BM25 funciona correctamente para el chunk curado.

### Problemas detectados

- El LLM local puede tardar demasiado en generar respuesta con preguntas largas.
- El endpoint puede registrar HTTP 200 aunque el cliente curl haya cortado por timeout.
- Resultados secundarios todavía incluyen ruido de OneLake Shortcuts.
- La recuperación principal es correcta, pero conviene mejorar filtrado o reducir ruido del corpus.

### Decisión

La ruta de ingestión mediante JSON chunks funciona.

Antes de añadir muchas fuentes, hay que mantener chunks muy específicos y controlar el ruido de recuperación.

### Siguiente acción recomendada

No tocar `api_rag_v2.py` todavía.

Siguiente mejora segura:

- crear más chunks curados solo si pasan criterios de curación;
- evitar contenido genérico;
- considerar en el futuro filtrado por `source`, `quality_score` o `block_type`;
- revisar latencia de Ollama como tarea separada.
