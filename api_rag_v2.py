from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from rag_loader import load_chunks
from rag_retriever import retrieve_chunks
from rag_intent import detect_intent
import urllib.parse, subprocess, re

API_TOKEN = "neodaemon-secure-token"

def clean_ansi(text):
    return re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', text)

def ask_llm(question):
    chunks = load_chunks()
    results = retrieve_chunks(chunks, question, top_k=5)

    if not results:
        return {
            "answer": "No se encontró contexto relevante.",
            "confidence": "low",
            "sources": []
        }

    context = "\n\n".join([r["text"] for r in results[:3]])

    prompt = f"""Eres experto en Microsoft Fabric.

Usa SOLO el contexto para responder.

Contexto:
{context}

Pregunta:
{question}

Respuesta clara y técnica:"""

    try:
        result = subprocess.run(
            ["ollama", "run", "llama3.2:3b"],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=240
        )

        raw_answer = result.stdout.strip()
        answer = clean_ansi(raw_answer)

        return {
            "answer": answer,
            "confidence": "high" if results[0]["score"] > 0.3 else "medium",
            "sources": [
                {
                    "score": r["score"],
                    "url": r.get("url"),
                    "chunk_id": r.get("chunk_id")
                }
                for r in results[:3]
            ]
        }

    except Exception as e:
        return {
            "answer": f"Error LLM: {e}",
            "confidence": "low",
            "sources": []
        }

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

        result = ask_llm(question)

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())

def main():
    server = HTTPServer(("127.0.0.1", 5001), Handler)
    print("API v2 running on 5001")
    server.serve_forever()

if __name__ == "__main__":
    main()
