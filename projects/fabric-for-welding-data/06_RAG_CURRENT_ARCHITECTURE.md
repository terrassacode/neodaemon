# 06_RAG_CURRENT_ARCHITECTURE

## Objetivo

Documentar el estado real del RAG local de OpenClaw usado por el proyecto fabric-for-welding-data.

## Fecha

2026-05-20

## Estado confirmado

El RAG operativo usa:

- API local: `/openclaw/api_rag_v2.py`
- Loader: `/openclaw/rag_loader.py`
- Retriever: `/openclaw/rag_retriever.py`
- Filtro: `/openclaw/rag_filter.py`
- LLM local: Ollama con modelo `llama3.2:3b`

## Flujo real confirmado

```text
pregunta
→ /rag-ask
→ ask_llm(question)
→ load_chunks()
→ retrieve_chunks(..., top_k=5)
→ filter_results(...)
→ contexto top 3
→ ollama run llama3.2:3b
→ respuesta JSON
```

## Fuente actual de chunks

El loader carga archivos JSON desde:

```text
/openclaw/workspace/main/rag_store/chunks_v2
```

Cada archivo JSON puede aportar:

- `text` o `content`
- `source`
- `url`
- `chunk_id`

## Retriever

El retriever usa BM25 mediante `rank_bm25`.

No se confirmó uso de embeddings, FAISS, Chroma u otro vector store en el flujo inspeccionado.

## Filtro

El filtro elimina:

- list_items pobres de menos de 200 caracteres;
- textos de menos de 80 caracteres.

## Punto clave

El contexto curado en GitHub/context_repo todavía no entra automáticamente al RAG.

Actualmente existe:

```text
GitHub/context_repo → memoria documental
load_context.sh → concatenador de contexto
rag_store/chunks_v2 → fuente real del RAG actual
```

Por tanto, para alimentar el RAG con el proyecto fabric-for-welding-data, el contenido curado debe convertirse a chunks JSON compatibles con `rag_loader.py` o modificarse el loader de forma controlada.

## Decisión técnica recomendada

No modificar todavía `/openclaw/api_rag_v2.py`.

Primero crear un proceso seguro para transformar conocimiento curado en JSON chunks dentro de:

```text
/openclaw/workspace/main/rag_store/chunks_v2
```

## Formato mínimo recomendado para nuevos chunks

```json
{
  "text": "contenido curado accionable",
  "source": "fabric-for-welding-data",
  "url": "https://...",
  "chunk_id": "fabric-fw-0001",
  "block_type": "curated_note",
  "title": "titulo",
  "quality_score": 0.9
}
```

## Riesgos

- Meter contenido sin curación puede contaminar el RAG.
- Duplicar información puede degradar BM25.
- Chunks demasiado cortos serán descartados por el filtro.
- Chunks demasiado largos pueden reducir precisión.
- El token local visto en api_rag_v2.py debería rotarse y externalizarse más adelante, pero no se abre esa tarea ahora.

## Siguiente acción recomendada

Crear un primer chunk JSON manual y controlado desde la fuente ya curada:

```text
Microsoft Real-Time Intelligence Operations Solution Accelerator
```

Validar después con una pregunta real:

```text
¿Cómo ayuda Fabric Real-Time Intelligence a detectar inestabilidad en soldadura?
```

## Estado

Inspección documentada.
No se ha modificado RAG.
No se han reiniciado servicios.
