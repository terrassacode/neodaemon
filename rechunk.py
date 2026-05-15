from pathlib import Path
import json

IN = Path("/openclaw/workspace/main/rag_store/chunks")
OUT = Path("/openclaw/workspace/main/rag_store/chunks_v2")

OUT.mkdir(parents=True, exist_ok=True)

for old in OUT.glob("*.json"):
    old.unlink()

i = 0
CHUNK_SIZE = 900
OVERLAP = 150

for f in IN.glob("*.json"):
    d = json.loads(f.read_text())
    text = d.get("text") or d.get("content") or ""

    text = " ".join(text.split())

    start = 0
    while start < len(text):
        part = text[start:start + CHUNK_SIZE].strip()
        if len(part) > 100:
            (OUT / f"chunk_{i}.json").write_text(json.dumps({"text": part}))
            i += 1
        start += CHUNK_SIZE - OVERLAP

print("Chunks nuevos:", i)
