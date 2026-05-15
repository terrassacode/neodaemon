import re
from rank_bm25 import BM25Okapi

def tokenize(text):
    return re.findall(r"[a-zA-Z0-9áéíóúüñÁÉÍÓÚÜÑ]+", text.lower())

def bm25_rank(chunks, query, top_k=5, min_score=0.0):
    if not chunks:
        return []

    tokenized = [tokenize(c) for c in chunks]
    bm25 = BM25Okapi(tokenized)
    scores = bm25.get_scores(tokenize(query))
    ranked = sorted(zip(scores, chunks), key=lambda x: x[0], reverse=True)

    return [
        {"score": float(score), "text": chunk}
        for score, chunk in ranked[:top_k]
        if score >= min_score
    ]

def retrieve_chunks(chunks, query, top_k=5, min_score=0.0):
    q = query.lower()

    # modo comparación: priorizar, no bloquear todo
    if "lakehouse" in q and "warehouse" in q:
        preferred = [
            c for c in chunks
            if "lakehouse" in c.lower()
            and "warehouse" in c.lower()
            and "shortcut" not in c.lower()
        ]

        if len(preferred) >= 2:
            return bm25_rank(preferred, query, top_k, min_score)

    return bm25_rank(chunks, query, top_k, min_score)
