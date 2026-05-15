import requests

def embed(text):
    r = requests.post(
        "http://127.0.0.1:11434/api/embeddings",
        json={
            "model": "nomic-embed-text",
            "prompt": text
        },
        timeout=60
    )
    return r.json()["embedding"]
