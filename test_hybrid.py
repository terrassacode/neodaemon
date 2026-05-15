from rag_loader import load_chunks
from rag_retriever import retrieve_chunks
from rag_embedder import embed
import math

def cosine(a, b):
    dot = sum(x*y for x, y in zip(a, b))
    na = math.sqrt(sum(x*x for x in a))
    nb = math.sqrt(sum(y*y for y in b))
    return dot / (na * nb) if na and nb else 0

q = "cuando usar lakehouse vs warehouse"
chunks = load_chunks()

bm25 = retrieve_chunks(chunks, q, top_k=10, min_score=0)

qv = embed(q)

scored = []
for r in bm25:
    cv = embed(r["text"][:2000])
    sim = cosine(qv, cv)
    hybrid = (0.6 * r["score"]) + (0.4 * sim)
    scored.append((hybrid, r["score"], sim, r["text"][:200]))

for h, b, s, text in sorted(scored, reverse=True)[:5]:
    print("HYBRID:", round(h, 3), "BM25:", round(b, 3), "SIM:", round(s, 3))
    print(text.replace("\n", " ")[:200])
    print("---")
