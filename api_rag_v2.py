from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from rag_loader import load_chunks
from rag_retriever import retrieve_chunks
from rag_intent import detect_intent
from rag_filter import filter_results
import urllib.parse, subprocess, re

API_TOKEN = "neodaemon-secure-token"


def clean_ansi(text):
    return re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', text)
def clean_ansi(text):
    return re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', text)


def clean_answer(text):
    # quitar saludos innecesarios
    text = text.replace("Excelente pregunta!", "").strip()

    # eliminar fragmento + palabra completa: "permi permite" -> "permite"
    text = re.sub(r'\b(\w{2,6})\s+(\1\w+)\b', r'\2', text, flags=re.IGNORECASE)

    # eliminar palabras duplicadas seguidas
    text = re.sub(r'\b(\w+)\s+\1\b', r'\1', text, flags=re.IGNORECASE)

    # arreglar cortes tipo "JS JSON" → "JSON"
    text = re.sub(r'\b[A-Z]{1,3}\s+([A-Z]{2,})\b', r'\1', text)

    # eliminar repeticiones de líneas
    lines = text.split("\n")
    cleaned = []
    for line in lines:
        if not cleaned or cleaned[-1] != line:
            cleaned.append(line)

    return "\n".join(cleaned).strip()
def ask_llm(question):
    chunks = load_chunks()
    results = retrieve_chunks(chunks, question, top_k=5)

    # 🔥 filtro de calidad
    results = filter_results(results)

    if not results:
        return {
            "answer": "No se encontró contexto relevante.",
            "confidence": "low",
            "sources": []
        }

    context = "\n\n".join([r["text"] for r in results[:3]])

    prompt = f"""Eres experto en Microsoft Fabric.
Usa el contexto para responder de forma clara y técnica.

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
        answer = clean_answer(clean_ansi(raw_answer))

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
