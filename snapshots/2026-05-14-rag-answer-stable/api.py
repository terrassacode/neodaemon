from http.server import BaseHTTPRequestHandler, HTTPServer
import json, os, re, urllib.parse, subprocess
from rank_bm25 import BM25Okapi

HOST = "0.0.0.0"
PORT = 5000
API_TOKEN = "neodaemon-secure-token"
CHUNKS_DIR = "/openclaw/workspace/main/rag_store/chunks"

def tokenize(text):
    return re.findall(r"\b\w+\b", text.lower())

def send_headers(handler, code=200, content_type="text/plain"):
    handler.send_response(code)
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
    handler.send_header("Access-Control-Allow-Headers", "*")
    handler.send_header("Content-Type", content_type)
    handler.end_headers()

def check_auth(path):
    params = urllib.parse.parse_qs(urllib.parse.urlparse(path).query)
    return params.get("token", [""])[0] == API_TOKEN

def load_index():
    docs = []
    tokenized = []
    for filename in os.listdir(CHUNKS_DIR):
        if not filename.endswith(".json"):
            continue
        with open(os.path.join(CHUNKS_DIR, filename), "r", encoding="utf-8") as f:
            chunk = json.load(f)
        docs.append(chunk)
        tokenized.append(tokenize(chunk.get("content", "")))
    return docs, BM25Okapi(tokenized)

DOCS, BM25 = load_index()

def ask_llm(context, question):
    prompt = f"""
You are an expert in Microsoft Fabric.

Use ONLY the context below to answer:

CONTEXT:
{context}

QUESTION:
{question}

Answer clearly and technically.
"""
    # usando tu entorno local (ollama o similar)
    result = subprocess.run(
        ["ollama", "run", "gemma4:26b-a4b-it-q4_K_M"],
        input=prompt.encode(),
        stdout=subprocess.PIPE
    )
    return result.stdout.decode()

class Handler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        send_headers(self, 200)

    def do_GET(self):

        if self.path == "/health":
            send_headers(self, 200)
            self.wfile.write(b"OK")
            return

        if not check_auth(self.path):
            send_headers(self, 401)
            self.wfile.write(b"Unauthorized")
            return

        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        params = urllib.parse.parse_qs(parsed.query)

        if path == "/rag-ask":
            question = params.get("q", [""])[0]

            scores = BM25.get_scores(tokenize(question))
            ranked = sorted(zip(scores, DOCS), key=lambda x: x[0], reverse=True)

            top_chunks = [chunk.get("content") for score, chunk in ranked[:3] if score > 0]
            context = "\n\n".join(top_chunks)

            answer = ask_llm(context, question)

            send_headers(self, 200, "application/json")
            self.wfile.write(json.dumps({
                "answer": answer
            }).encode())
            return

        send_headers(self, 404)
        self.wfile.write(b"Not Found")

if __name__ == "__main__":
    print(f"Loaded {len(DOCS)} chunks")
    server = HTTPServer((HOST, PORT), Handler)
    print(f"API running on http://{HOST}:{PORT}")
    server.serve_forever()
