from http.server import BaseHTTPRequestHandler, HTTPServer
import json, urllib.parse, subprocess

API_TOKEN = "neodaemon-secure-token"

def ask_llm(question):
    try:
        result = subprocess.run(
            ["ollama", "run", "llama3.1:8b", question],
            capture_output=True,
            text=True,
            timeout=120
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
    server = HTTPServer(("127.0.0.1", 5000), Handler)
    print("API running on 5000")
    server.serve_forever()

if __name__ == "__main__":
    main()
