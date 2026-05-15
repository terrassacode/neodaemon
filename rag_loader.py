import json
from pathlib import Path

CHUNKS_DIR = "/openclaw/workspace/main/rag_store/chunks_v2"

def load_chunks():
    chunks = []
    for f in Path(CHUNKS_DIR).glob("*.json"):
        try:
            d = json.loads(f.read_text())
            text = d.get("text") or d.get("content") or ""
            if text:
                chunks.append({
                    "text": text,
                    "source": d.get("source", ""),
                    "url": d.get("url", ""),
                    "chunk_id": d.get("chunk_id", "")
                })
        except:
            continue
    return chunks
