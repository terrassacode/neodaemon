from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from rag_loader import load_chunks
from rag_retriever import retrieve_chunks
import urllib.parse, subprocess
from pathlib import Path

API_TOKEN = "neodaemon-secure-token"
CHUNKS_DIR = "/openclaw/workspace/main/rag_store/chunks"



def rank_chunks(chunks, query):
    query = query.lower()
    scored = []
    for c in chunks:
        score = sum(1 for w in query.split() if w in c.lower())
        scored.append((score, c))
    return [c for score, c in sorted(scored, reverse=True)[:5] if score > 0]

def ask_llm(question):
    chunks = load_chunks()
    results = retrieve_chunks(chunks, question, top_k=5)
    context = "\n\n".join([r["text"] for r in results[:3]])

    prompt = f"""Contexto:
{context}

Pregunta:
{question}

Respuesta:"""

    try:
        result = subprocess.run(
            ["ollama", "run", "llama3.2:3b", "--nowordwrap"],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=240
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Error LLM: {e}"

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path != "/rag-ask":
            self.send_response(404)
            self.end_headers()
            return

        params = urllib.parse.parse_qs(parsed.query)
        token = params.get("token", [""])[0]
        question = params.get("q", [""])[0]

        if token != API_TOKEN:
            self.send_response(403)
            self.end_headers()
            return

        answer = ask_llm(question)

        resp = {
            "answer": answer,
            "confidence": "low",
            "score_max": 0
        }

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(resp).encode())

def main():
    server = HTTPServer(("127.0.0.1", 5001), Handler)
    print("API running on 5001")
    server.serve_forever()

if __name__ == "__main__":
    main()
