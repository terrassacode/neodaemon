import json
import time
from pathlib import Path

STRUCTURED = Path("/openclaw/workspace/main/rag_store/structured")
CHUNKS = Path("/openclaw/workspace/main/rag_store/chunks_v2")
LOG = Path("/openclaw/workspace/main/logs/rag_web/chunk_structured.log")

CHUNKS.mkdir(parents=True, exist_ok=True)
LOG.parent.mkdir(parents=True, exist_ok=True)

created = 0

for f in STRUCTURED.glob("*.json"):
    d = json.loads(f.read_text(encoding="utf-8"))

    if d.get("quality_score", 0) < 60:
        continue

    for i, block in enumerate(d.get("blocks", [])):
        content = block.get("content", "").strip()

        if len(content) < 80:
            continue

        chunk = {
            "text": content,
            "source": "internet_curated",
            "url": d.get("url"),
            "title": d.get("title"),
            "source_type": d.get("source_type"),
            "category": d.get("category"),
            "block_type": block.get("type"),
            "quality_score": d.get("quality_score"),
            "chunk_id": f"{f.stem}_block_{i}"
        }

        out = CHUNKS / f"{f.stem}_block_{i}.json"
        out.write_text(json.dumps(chunk, ensure_ascii=False, indent=2), encoding="utf-8")
        created += 1

LOG.open("a", encoding="utf-8").write(
    f"{time.strftime('%Y-%m-%d %H:%M:%S')} created={created}\n"
)

print(f"Chunks creados: {created}")
