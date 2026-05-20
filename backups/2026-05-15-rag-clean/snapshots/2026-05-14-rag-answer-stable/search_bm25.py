import os, json, sys, re
from rank_bm25 import BM25Okapi

CHUNKS_DIR = "/openclaw/workspace/main/rag_store/chunks"

query = " ".join(sys.argv[1:])
if not query:
    print('Uso: python3 search_bm25.py "consulta"')
    sys.exit(1)

def tokenize(text):
    return re.findall(r"\b\w+\b", text.lower())

docs = []
tokenized = []

for filename in os.listdir(CHUNKS_DIR):
    if not filename.endswith(".json"):
        continue
    path = os.path.join(CHUNKS_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        chunk = json.load(f)
    docs.append(chunk)
    tokenized.append(tokenize(chunk.get("content", "")))

bm25 = BM25Okapi(tokenized)
scores = bm25.get_scores(tokenize(query))

ranked = sorted(zip(scores, docs), key=lambda x: x[0], reverse=True)

for score, chunk in ranked[:5]:
    if score <= 0:
        continue
    print("=" * 80)
    print(f"Score: {score:.3f}")
    print(f"Title: {chunk.get('title')}")
    print(f"Source: {chunk.get('source')}")
    print(f"URL: {chunk.get('url')}")
    print(f"Chunk: {chunk.get('chunk_id')}")
    print("-" * 80)
    print(chunk.get("content", "")[:900])
    print()
