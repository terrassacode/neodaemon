import json
import requests
import subprocess
import hashlib
from pathlib import Path

APPROVED = Path("/openclaw/workspace/main/rag_store/approved")
CLASSIFIED = APPROVED / "classified"

CATEGORIES = {
    "fabric": ["fabric", "onelake", "lakehouse", "warehouse"],
    "ai": ["ai", "machine learning", "llm"],
    "data": ["data engineering", "pipeline", "etl"]
}


def content_hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def already_exists(hash_value):
    for f in CLASSIFIED.rglob("*.txt"):
        if f.name.startswith(hash_value):
            return True
    return False

def classify(text):
    t = text.lower()
    for cat, keywords in CATEGORIES.items():
        for k in keywords:
            if k in t:
                return cat
    return "other"

def fetch_text(url):
    try:
        from bs4 import BeautifulSoup
        import re

        r = requests.get(url, timeout=25, headers={
            "User-Agent": "Mozilla/5.0 NeodaemonRAG"
        })

        soup = BeautifulSoup(r.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer", "header", "noscript"]):
            tag.decompose()

        text = soup.get_text("\n")
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = re.sub(r"[ \t]+", " ", text)
        text = text.strip()

        return text[:12000]
    except Exception:
        return ""

def process_file(p):
    data = json.loads(p.read_text())
    url = data["url"]

    text = fetch_text(url)
    if not text:
        return False

    cat = classify(text)

    out_dir = CLASSIFIED / cat
    out_dir.mkdir(parents=True, exist_ok=True)

    h = content_hash(text)
    if already_exists(h):
        p.unlink()
        return False

    name = h + "_" + p.stem + ".txt"
    out_path = out_dir / name
    out_path.write_text(text)

    p.unlink()  # elimina de approved
    return True

def rebuild():
    subprocess.run([
        "/openclaw/venvs/api/bin/python",
        "/openclaw/workspace/main/rag_store/build_vector_index.py"
    ])

def main():
    files = list(APPROVED.glob("*.json"))

    done = 0
    for f in files:
        if process_file(f):
            done += 1

    if done:
        rebuild()

    print(f"Processed: {done}")

if __name__ == "__main__":
    main()
