from http.server import BaseHTTPRequestHandler, HTTPServer
import json, os, re, urllib.parse, subprocess, datetime, math
import requests
from rank_bm25 import BM25Okapi

API_TOKEN = "neodaemon-secure-token"
CHUNKS_DIR = "/openclaw/workspace/main/rag_store/chunks"

MIN_SCORE = 0.20



def normalize_query(q):
    q = q.lower()
    replacements = {
        "wharehouse": "warehouse",
        "warehosue": "warehouse",
        "lake house": "lakehouse",
        "one lake": "onelake"
    }
    for k, v in replacements.items():
        q = q.replace(k, v)

    # normalización semántica
    if "lago de datos" in q or "lake" in q:
        q = q.replace("lago de datos", "lakehouse")

    if "almacén" in q or "almacen" in q:
        q = q.replace("almacén", "warehouse")
        q = q.replace("almacen", "warehouse")

    if "diferencia" in q and "warehouse" in q and "lakehouse" in q:
        q = "difference between lakehouse and warehouse in microsoft fabric"

    if "warehouse" in q and "fabric" not in q:
        q = q + " microsoft fabric"

    if "lakehouse" in q and "fabric" not in q:
        q = q + " microsoft fabric"

    if "onelake" in q and "fabric" not in q:
        q = q + " microsoft fabric"

    return q

def tokenize(text):
    return re.findall(r"\b\w+\b", text.lower())

def send(handler, code=200, data="", content_type="text/plain"):
    handler.send_response(code)
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Content-Type", content_type)
    handler.end_headers()
    handler.wfile.write(data if isinstance(data, bytes) else data.encode())

def load_index():
    docs, tokenized = [], []
    for f in os.listdir(CHUNKS_DIR):
        if not f.endswith(".json"):
            continue
        with open(os.path.join(CHUNKS_DIR, f), encoding="utf-8") as fh:
            chunk = json.load(fh)
        docs.append(chunk)
        tokenized.append(tokenize(chunk.get("content", "")))
    return docs, BM25Okapi(tokenized)

DOCS, BM25 = load_index()

VECTOR_INDEX = "/openclaw/workspace/main/rag_store/vector/index.jsonl"

def embed_query(text):
    r = requests.post("http://127.0.0.1:11434/api/embeddings", json={
        "model": "nomic-embed-text",
        "prompt": text
    }, timeout=120)
    r.raise_for_status()
    return r.json()["embedding"]

def cosine(a, b):
    dot = sum(x*y for x, y in zip(a, b))
    na = math.sqrt(sum(x*x for x in a))
    nb = math.sqrt(sum(x*x for x in b))
    return dot / (na * nb)

def vector_search(query, min_score=0.40):
    try:
        q_vec = embed_query(query)
        data = [json.loads(l) for l in open(VECTOR_INDEX)]
        scored = [(cosine(q_vec, d["embedding"]), d) for d in data]
        top = sorted(scored, key=lambda x: x[0], reverse=True)[:3]
        return [(score, d) for score, d in top if score >= min_score]
    except Exception:
        return []




def log_query(question, score, confidence, chunks, sources, answer):
    try:
        log_path = "/openclaw/logs/rag_queries.jsonl"
        entry = {
            "ts": datetime.datetime.utcnow().isoformat(),
            "question": question,
            "score_max": float(score),
            "confidence": confidence,
            "chunks_used": chunks,
            "sources": [s.get("url") for s in sources],
            "answer_chars": len(answer)
        }
        with open(log_path, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except:
        pass

def ask_llm(context, question):
    prompt = f"""
Responde SOLO usando el contexto proporcionado.

Formato obligatorio:

Definición:
(explicación clara y técnica en 2-3 líneas)

Características clave:
- punto clave 1
- punto clave 2
- punto clave 3

Cuándo usarlo:
- caso 1
- caso 2

Limitación del contexto:
(indica si la respuesta puede ser incompleta)

Reglas:
- No inventes información
- No introduzcas conceptos que no estén literalmente respaldados por el contexto\n- No uses términos como NoSQL, OLAP, tiempo real o data mesh salvo que aparezcan claramente en el contexto
- Si no estás seguro, responde: "No hay suficiente contexto para responder con precisión"

Contexto:
{context}

Pregunta:
{question}

Respuesta:
"""
    try:
        r = requests.post("http://127.0.0.1:11434/api/generate", json={
            "model": "llama3.2:3b",
            "prompt": prompt,
            "stream": False
        }, timeout=120)
        return r.json().get("response", "").strip()
    except Exception as e:
        return "Error LLM: " + str(e)

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        p = urllib.parse.urlparse(self.path)
        path = p.path
        q = urllib.parse.parse_qs(p.query)

        if path == "/health":
            return send(self, 200, "OK")

        if q.get("token", [""])[0] != API_TOKEN:
            return send(self, 401, "Unauthorized")

        if path == "/rag-ask":
            question = q.get("q", [""])[0].strip()
            question = normalize_query(question)

            if not question:
                return send(self, 400, json.dumps({
                    "error": "missing_question",
                    "answer": "Introduce una pregunta."
                }), "application/json")

            scores = BM25.get_scores(tokenize(question))
            ranked = sorted(zip(scores, DOCS), key=lambda x: x[0], reverse=True)

            candidates = []

            for score, c in ranked[:5]:
                if score >= MIN_SCORE:
                    candidates.append({
                        "content": c.get("content", ""),
                        "score": float(score),
                        "title": c.get("title"),
                        "source": c.get("source"),
                        "url": c.get("url")
                    })

            for score, d in vector_search(question):
                candidates.append({
                    "content": d.get("content", ""),
                    "score": float(score),
                    "title": d.get("title"),
                    "source": d.get("source"),
                    "url": d.get("url")
                })

            candidates = sorted(candidates, key=lambda x: x["score"], reverse=True)

            seen_content = set()
            top_chunks = []
            top_meta = []

            for c in candidates:
                content = c.get("content", "")
                if not content or content in seen_content:
                    continue
                seen_content.add(content)
                top_chunks.append(content)
                top_meta.append(c)
                if len(top_chunks) == 3:
                    break

            if not top_chunks:
                return send(self, 200, json.dumps({
        "answer": "No he encontrado contexto relevante para responder con precisión.",
        "confidence": "low",
        "score_max": 0.0,
        "chunks_used": 0,
        "sources": []
    }), "application/json")

            context = "\n\n".join(top_chunks)
            answer = ask_llm(context, question)

            max_score = max([c["score"] for c in top_meta]) if top_meta else 0.0

            if max_score < 0.30:
                return send(self, 200, json.dumps({
        "answer": "No hay suficiente contexto relevante para responder con fiabilidad.",
        "confidence": "low",
        "chunks_used": len(top_chunks),
        "score_max": float(max_score),
        "sources": []
    }), "application/json")
            elif max_score < 0.60:
                confidence = "medium"
            else:
                confidence = "high"

            seen_urls = set()
            sources = []

            for c in top_meta:
                url = c.get("url")
                if not url or url in seen_urls:
                    continue
                seen_urls.add(url)
                sources.append({
                    "title": c.get("title"),
                    "source": c.get("source"),
                    "url": url
                })

            log_query(question, max_score, confidence, len(top_chunks), sources, answer)

            return send(self, 200, json.dumps({
                "answer": answer,
                "chunks_used": len(top_chunks),
                "score_max": float(max_score),
                "confidence": confidence,
                "sources": sources
            }), "application/json")

        if path == "/rag-stats":
            import collections
            log_path = "/openclaw/logs/rag_queries.jsonl"

            stats = {
                "total": 0,
                "confidence": {"low": 0, "medium": 0, "high": 0}
            }

            try:
                with open(log_path) as f:
                    for line in f:
                        stats["total"] += 1
                        try:
                            j = json.loads(line)
                            c = j.get("confidence")
                            if c in stats["confidence"]:
                                stats["confidence"][c] += 1
                        except:
                            pass
            except:
                pass

            return send(self, 200, json.dumps(stats), "application/json")

        if path == "/summary":
            result = subprocess.check_output(["/openclaw/logs/daily_summary.sh"])
            return send(self, 200, result)

        if path == "/last-events":
            result = subprocess.check_output(["tail", "-n", "10", "/openclaw/logs/runtime/events.jsonl"])
            return send(self, 200, result)

        if path == "/restart-dashboard":
            subprocess.Popen(["systemctl", "--user", "restart", "openclaw-dashboard.service"])
            return send(self, 200, "Dashboard restarted")

        if path == "/restart-gateway":
            subprocess.Popen(["systemctl", "--user", "restart", "openclaw-gateway.service"])
            return send(self, 200, "Gateway restarted")

        return send(self, 404, "Not Found")

print("API ready")
HTTPServer(("0.0.0.0", 5000), H).serve_forever()