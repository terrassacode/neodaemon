import json
from pathlib import Path

CHUNKS_DIR = "/openclaw/workspace/main/rag_store/chunks_v2"

def load_chunks():
    chunks = []
    for f in Path(CHUNKS_DIR).glob("*.json"):
        try:
            d = json.loads(f.read_text())
            text = d.get("text") or d.get("content") or ""
            t = text.lower()

            # filtro global dataset
            if "shortcut" in t or "onelake" in t:
                continue

            if text:
                chunks.append(text)
        except:
            continue
    return chunks
