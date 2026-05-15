import os, json

IN_DIR = "/openclaw/workspace/main/rag_store/cleaned"
OUT_DIR = "/openclaw/workspace/main/rag_store/chunks"

os.makedirs(OUT_DIR, exist_ok=True)

CHUNK_SIZE = 500  # palabras

for name in os.listdir(IN_DIR):
    if not name.endswith(".json"):
        continue

    path = os.path.join(IN_DIR, name)

    with open(path, "r", encoding="utf-8") as f:
        doc = json.load(f)

    words = doc["content"].split()
    chunks = [words[i:i+CHUNK_SIZE] for i in range(0, len(words), CHUNK_SIZE)]

    for i, chunk in enumerate(chunks):
        out = {
            "source": doc["source"],
            "url": doc["url"],
            "title": doc["title"],
            "domain": doc["domain"],
            "chunk_id": f"{name}_{i}",
            "content": " ".join(chunk)
        }

        with open(f"{OUT_DIR}/{name}_{i}.json", "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)

print("Chunking completado")
