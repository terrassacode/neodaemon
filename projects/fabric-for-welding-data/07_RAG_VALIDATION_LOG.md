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

### Resultado técnico

El endpoint `/rag-ask` respondió con HTTP 200 y devolvió respuesta JSON.

El primer resultado recuperado fue el chunk nuevo:

```text
chunk_id: fabric_rti_operations_accelerator_001
score: 10.04 aprox.
```

### Conclusión

El RAG actual sí consume nuevos archivos JSON añadidos a `rag_store/chunks_v2` sin necesidad de modificar `api_rag_v2.py` ni reiniciar servicios.

### Calidad de respuesta

Resultado mixto:

- Recuperación: correcta.
- Respuesta: demasiado genérica.
- Problema detectado: el LLM generaliza hacia sensores genéricos como temperatura, aceleración o presión, en lugar de centrarse en RD, variabilidad, robot, programa, corriente y esfuerzo.
- Ruido adicional: también recuperó chunks no relacionados de OneLake Shortcuts como segunda y tercera fuente.

### Decisión

La ruta de ingestión mediante JSON chunks funciona.

Antes de añadir muchas fuentes, hay que mejorar la especificidad del chunk y/o el filtrado para evitar respuestas genéricas.

### Siguiente acción recomendada

Crear chunks más explícitos y orientados a soldadura:

- mencionar RD varias veces;
- incluir variabilidad de RD;
- incluir robot/programa;
- evitar vocabulario genérico de sensores si no aplica;
- separar arquitectura Fabric de lógica industrial.

Después repetir la prueba con una pregunta controlada.
