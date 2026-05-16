import re
from rank_bm25 import BM25Okapi

def tokenize(text):
    return re.findall(r"[a-zA-Z0-9áéíóúüñÁÉÍÓÚÜÑ]+", text.lower())

def get_text(chunk):
    if isinstance(chunk, dict):
        return chunk.get("text", "")
    return str(chunk)

def bm25_rank(chunks, query, top_k=5, min_score=0.0):
    if not chunks:
        return []

    tokenized = [tokenize(get_text(c)) for c in chunks]
    bm25 = BM25Okapi(tokenized)
    scores = bm25.get_scores(tokenize(query))

    ranked = sorted(zip(scores, chunks), key=lambda x: x[0], reverse=True)

    results = []
    for score, chunk in ranked[:top_k]:
        if score >= min_score:
            text = get_text(chunk)
            results.append({
                "score": float(score),
                "text": text,
                "source": chunk.get("source", "") if isinstance(chunk, dict) else "",
                "url": chunk.get("url", "") if isinstance(chunk, dict) else "",
                "chunk_id": chunk.get("chunk_id", "") if isinstance(chunk, dict) else "",
                "block_type": chunk.get("block_type", "") if isinstance(chunk, dict) else "",
                "title": chunk.get("title", "") if isinstance(chunk, dict) else "",
                "quality_score": chunk.get("quality_score", 0) if isinstance(chunk, dict) else 0
            })

    return results

def retrieve_chunks(chunks, query, top_k=5, min_score=0.0):
    q = query.lower()

    if "lakehouse" in q and "warehouse" in q:
        preferred = [
            c for c in chunks
            if "lakehouse" in get_text(c).lower()
            and "warehouse" in get_text(c).lower()
            and "shortcut" not in get_text(c).lower()
        ]
        if len(preferred) >= 2:
            return bm25_rank(preferred, query, top_k, min_score)

    return bm25_rank(chunks, query, top_k, min_score)
