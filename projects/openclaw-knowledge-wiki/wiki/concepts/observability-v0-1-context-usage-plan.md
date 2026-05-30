# Observability v0.1 Context Usage Plan

## Estado

Roadmap creado.

## Propósito

Definir una estrategia mínima de observabilidad para comprender cómo Neodaemon utiliza contexto durante la toma de decisiones.

El objetivo no es medir costes económicos ni tokens exactos.

El objetivo es medir:

- qué contexto se carga;
- con qué frecuencia se carga;
- qué contexto se evita cargar;
- dónde existen redundancias.

## Problema observado

Actualmente existen datos parciales sobre uso de recursos.

Sin embargo:

- las métricas disponibles están desactualizadas;
- no existe trazabilidad fiable de carga de contexto;
- no existe correlación con decisiones;
- no existe medición de ahorro de contexto.

Como consecuencia, no puede determinarse con evidencia:

```text
si existe consumo excesivo de tokens
```

pero tampoco puede demostrarse:

```text
que el sistema esté utilizando el contexto de forma eficiente
```

## Evidencia recogida

Observaciones realizadas sobre el sistema:

```text
main/sessions ≈ 203 MB
task-validator/sessions ≈ 9,7 MB
246 archivos jsonl/jsonl*
23 backups/checkpoints
≈ 103,6 MB en backups/checkpoints
telegram-main activo ≈ 8,8 MB
```

Además:

- no se encontraron evidencias de rate limit;
- no se encontraron evidencias de errores 429;
- no existe una fuente actualizada de model calls recientes;
- se observaron lecturas repetidas de documentos de wiki.

## Hallazgo principal

La principal incertidumbre no es:

```text
cuántos tokens se consumen
```

La principal incertidumbre es:

```text
qué contexto se carga realmente
```

y:

```text
cuántas veces se vuelve a cargar
```

## Principio central

Toda optimización futura debe basarse en evidencia observable.

Regla:

```text
medir primero
optimizar después
```

## Objetivos

- identificar cargas redundantes;
- identificar documentos calientes;
- medir reutilización de summaries;
- estimar ahorro de contexto;
- relacionar contexto con decisiones;
- detectar crecimiento anómalo de sesiones;
- preparar futuras optimizaciones basadas en evidencia.

## Fuera de alcance

Esta versión no pretende medir:

- costes económicos;
- facturación de proveedores;
- precios por token;
- rendimiento de modelos;
- calidad de respuestas.

Tampoco implementa:

- dashboards;
- automatización;
- limpieza de sesiones;
- borrado automático.

## Métricas mínimas

La observabilidad debe centrarse en pocas métricas de alto valor.

### Context Load Frequency

Mide cuántas veces se carga un mismo contexto.

Objetivo:

```text
identificar documentos calientes
```

Ejemplos:

- wiki/log.md
- wiki/index.md
- summaries
- documentos de diseño

### Summary Hit Rate

Mide cuándo un summary evita cargar el documento fuente.

Éxito:

```text
summary_loaded
source_doc_not_loaded
```

Fracaso:

```text
summary_loaded
source_doc_loaded
```

### Context Saved Estimate

Estimación simple del contexto evitado.

Objetivo:

```text
medir ahorro
```

No precisión absoluta.

### Decision Correlation

Toda métrica debe poder relacionarse con:

```text
request_id
decision_id
```

para identificar qué decisiones consumen más contexto.

## Distinción obligatoria

No debe confundirse:

```text
file_read
```

con:

```text
context_loaded
```

Leer un archivo no implica necesariamente cargarlo en contexto.

La observabilidad debe registrar ambos eventos por separado.

## Clasificación de sesiones

Las sesiones deben clasificarse como:

```text
ACTIVE
ARCHIVE
DISPOSABLE
```

Objetivo:

- facilitar retención futura;
- evitar acumulación innecesaria;
- preservar sesiones relevantes.

## Reglas de observabilidad

### Privacidad

No registrar:

- prompts completos;
- contenido de archivos;
- secretos;
- tokens;
- credenciales;
- variables sensibles.

La observabilidad debe registrar únicamente metadatos.

### Retención

No eliminar sesiones automáticamente.

Primero debe existir evidencia suficiente para definir una política de retención.

### Evidencia antes que hipótesis

Regla principal:

```text
medir primero
optimizar después
```

No deben realizarse cambios de compactación o limpieza basados únicamente en intuiciones.

## Riesgos

### Riesgo 1

Confundir almacenamiento con consumo de contexto.

Mitigación:

```text
storage ≠ context_loaded
```

### Riesgo 2

Generar más datos de los que se observan.

Mitigación:

```text
eventos mínimos
```

### Riesgo 3

Optimizar sin evidencia.

Mitigación:

```text
usar métricas observables
```

## Decisión estratégica

La observabilidad v0.1 debe responder tres preguntas:

```text
qué contexto se carga
cuántas veces se carga
cuánto contexto conseguimos evitar
```

No pretende medir costes ni tokens exactos.

## Próximo paso recomendado

Crear una especificación operativa mínima para:

```text
context_load_frequency
summary_hit_rate
context_saved_estimate
decision_correlation
```

Antes de cualquier implementación.

La observabilidad debe permanecer pasiva, simple y basada en evidencia.


