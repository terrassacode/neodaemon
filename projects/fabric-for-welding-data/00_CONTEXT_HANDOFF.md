# CONTEXT HANDOFF — OpenClaw RAG Welding System

## Objetivo

Este archivo permite abrir un nuevo chat y continuar el proyecto sin empezar desde cero.

Debe ser leído al inicio de un nuevo chat como contexto base.

---

## Estado actual

- OpenClaw corre en VM `bunker-ia`.
- RAG API v2 está operativo.
- BM25 está validado.
- Wrappers `rag_ops` funcionan.
- Hay snapshot remoto en `terrassacode/neodaemon`.
- P2 no está cerrada.
- Fase actual: `P2A — Base de dominio soldadura / RD / BOSCH`.

---

## Objetivo técnico del RAG

Construir un RAG técnico fiable para soldadura por puntos, RD/resistencia dinámica y contexto industrial/BOSCH.

El sistema debe evitar respuestas genéricas o inventadas.

---

## Problema actual

La infraestructura funciona, pero falta conocimiento real de dominio.

Problemas observados:

- el modelo inventa `RD_factor`;
- pierde el valor `1.5`;
- degrada `std_RD_actual` y `std_RD_baseline`;
- genera KQL no curado;
- responde sin suficiente base real de soldadura.

Conclusión:

```text
El problema no está principalmente en BM25 ni wrappers.
Está en falta de conocimiento real de dominio y generación del modelo.
```

---

## Chunks técnicos relevantes

Chunks importantes existentes:

```text
fabric_rti_operations_accelerator_001
fabric_kql_rd_window_std_001
fabric_kql_rd_baseline_criteria_001
fabric_rd_baseline_answer_contract_001
```

La query de validación:

```text
std_RD_actual std_RD_baseline RobotId ProgramId 1.5 RD_factor no inventar nombres técnicos
```

recuperó como primer resultado:

```text
fabric_rd_baseline_answer_contract_001
```

BM25 funciona, pero la generación aún falla.

---

## Wrappers disponibles

Ruta oficial actual:

```text
/openclaw/workspace/main/context_repo/scripts/rag_ops/
```

Wrappers:

```text
rag_status_readonly.sh
rag_count_chunks.sh
rag_py_compile.sh
rag_test_bm25.sh
rag_query_local.sh
```

Reglas:

- usar wrappers oficiales;
- no pedir comandos libres si existe wrapper;
- usar el último `STATUS=` como estado final;
- leer `RESULT=` como resultado principal;
- `rag_query_local.sh` requiere autorización explícita.

---

## Fase actual: P2A

Objetivo:

```text
Introducir conocimiento técnico real desde PDF/manuales mediante curación manual asistida.
```

No hacer todavía:

- ingestion automática de PDF;
- split por tokens;
- creación masiva de chunks;
- extractor;
- embeddings;
- tocar `api_rag_v2.py`;
- reiniciar servicios.

---

## Pipeline aceptado para PDF técnico

1. Extraer texto del PDF a zona temporal.
2. No meter texto extraído directamente al RAG.
3. Segmentar por unidad de conocimiento, no por tamaño.
4. Crear chunks candidatos pequeños.
5. Revisar manualmente.
6. Clasificar con validation A/B/C/D.
7. Controlar status operativo.
8. Validar BM25 antes de integrar.
9. Integrar solo chunks aprobados.
10. Crear snapshot/commit después de estado bueno.

---

## Principio de chunking

No se trocea por tamaño.

Se trocea por:

```text
unidad de conocimiento autocontenida
```

Un chunk debe responder a una pregunta concreta.

Si responde a más de una pregunta, probablemente está mal.

---

## Esquema provisional de chunk técnico v0.1

No está congelado todavía.

```json
{
  "chunk_id": "tech_rd_001",
  "topic": "rd",
  "subtopic": "causas_alta",
  "title": "RD alta por contaminación de electrodos",
  "content": "La resistencia dinámica alta puede estar causada por contaminación en los electrodos, lo que aumenta la resistividad en la interfaz.",
  "keywords": ["RD alta", "resistencia dinamica alta", "contaminacion electrodos"],
  "query_patterns": ["por que sube la RD", "causas RD alta", "resistencia dinamica alta motivos"],
  "source": "bosch_manual_x.pdf",
  "page": 12,
  "layer": "technical",
  "validation": "A",
  "status": "approved",
  "applicability": "general",
  "risk_note": ""
}
```

---

## Validación y estado operativo

### validation

Mide calidad técnica:

```text
A = válido y fiable
B = válido pero condicionado
C = dudoso / requiere revisión
D = descartado
```

### status

Mide estado operativo:

```text
draft
review
approved
quarantine
deprecated
```

Relación aceptada:

```text
A → approved
B → review | approved
C → quarantine
D → no se guarda como chunk
```

---

## Regla B + approved

Un chunk `B + approved` solo se permite si:

- `risk_note` existe;
- `applicability` no es `general`;
- el chunk no formula una verdad universal;
- el contenido deja claro que está condicionado.

Ejemplo:

```json
{
  "validation": "B",
  "status": "approved",
  "applicability": "condicional",
  "risk_note": "Depende del estado del electrodo"
}
```

---

## Siguiente paso exacto

No continuar con PDF todavía.

No crear chunks masivos.

No hacer extractor.

Siguiente tarea:

```text
Definir reglas exactas A/B/C para chunks técnicos de soldadura/RD.
```

Debe incluir:

- criterios objetivos;
- ejemplos reales en soldadura por puntos;
- cuándo B puede subir a A;
- cuándo un chunk debe bajar a C;
- cómo tratar B + approved con `risk_note` y `applicability`;
- casos que deben descartarse como D.

---

## Forma de trabajo requerida

- pasos cortos;
- no avanzar sin OK;
- pensamiento crítico;
- no asentir por defecto;
- evitar respuestas genéricas;
- no empezar desde cero;
- continuar desde las reglas A/B/C.

---

## Red flags

Corregir al chat si propone:

- ingestion automática;
- split por tokens;
- embeddings antes de curación;
- respuestas genéricas tipo “depende del contexto” sin criterios;
- avanzar al PDF antes de cerrar reglas A/B/C.

---

## Punto exacto de continuación

Continuar aquí:

```text
Definir reglas exactas A/B/C para chunks técnicos de soldadura/RD antes de tocar PDF.
```
