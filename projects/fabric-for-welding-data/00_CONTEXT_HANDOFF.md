# CONTEXT HANDOFF — OpenClaw RAG Welding System

## 🎯 Objetivo del sistema

Construir un sistema basado en RAG que permita:

- interpretar datos de soldadura por puntos
- explicar comportamientos de RD (resistencia dinámica)
- detectar causas de inestabilidad
- generar respuestas técnicas fiables (no genéricas)

---

## 🧠 Estado actual del sistema

### Infraestructura

- OpenClaw en VM (bunker-ia)
- RAG v2 operativo
- endpoint `/rag-ask` funcional
- servicio systemd activo (`openclaw-rag-v2.service`)

### Recuperación

- BM25 validado
- recuperación correcta de chunks relevantes
- test BM25 OK

### Wrappers operativos

- `rag_status_readonly.sh`
- `rag_count_chunks.sh`
- `rag_test_bm25.sh`
- `rag_query_local.sh`

### Corpus

- ~40+ chunks en `/rag_store/chunks_v2`
- incluye:
  - baseline RD
  - window std
  - RTI accelerator
  - contract chunk (baseline 1.5)

---

## ⚠️ Problema actual

El sistema funciona técnicamente pero:

```text
NO tiene conocimiento real de soldadura
