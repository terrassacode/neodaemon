import json
import subprocess
import re
import hashlib
import requests
from pathlib import Path
from bs4 import BeautifulSoup

APPROVED = Path("/openclaw/workspace/main/rag_store/approved")
CLASSIFIED = APPROVED / "classified"

def url_hash(url):
    import hashlib
    return hashlib.sha256(url.encode("utf-8")).hexdigest()

def content_hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def clean_html(url):
    r = requests.get(url, timeout=25, headers={"User-Agent": "Mozilla/5.0 NeodaemonRAG"})
    soup = BeautifulSoup(r.text, "html.parser")

    for tag in soup(["script", "style", "nav", "footer", "header", "noscript"]):
        tag.decompose()

    url_lower = url.lower()

    if "community.fabric.microsoft.com" in url_lower:
        main = soup.find("div", {"class": "lia-message-body-content"})
        if main:
            text = main.get_text("\n")
        else:
            text = soup.get_text("\n")
    else:
        text = soup.get_text("\n")

    import re
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)

    return text.strip()[:12000]

def clean_vtt(path):
    text = path.read_text(errors="ignore")
    text = re.sub(r"\d{2}:\d{2}:\d{2}\.\d{3} --> .*", "", text)
    text = re.sub(r"WEBVTT.*?\n\n", "", text, flags=re.DOTALL)
    text = re.sub(r"<.*?>", "", text)
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    return " ".join(lines)[:12000]

def process_youtube(url, out_dir):
    tmp = Path("/tmp/neodaemon_youtube")
    tmp.mkdir(exist_ok=True)

    subprocess.run([
        "yt-dlp",
        "--skip-download",
        "--write-auto-subs",
        "--sub-langs", "en-orig,en,es",
        "--sub-format", "vtt",
        "-o", str(tmp / "%(id)s.%(ext)s"),
        url
    ], check=False)

    vtts = sorted(tmp.glob("*.vtt"), key=lambda x: x.stat().st_mtime, reverse=True)
    if not vtts:
        return ""

    text = clean_vtt(vtts[0])

    # limpiar temporales
    for f in tmp.glob("*"):
        f.unlink()

    return text

def save_text(text, meta, category):
    if not text:
        return False

    out_dir = CLASSIFIED / category
    out_dir.mkdir(parents=True, exist_ok=True)

    h = content_hash(text)
    for f in CLASSIFIED.rglob("*.txt"):
        if f.name.startswith(h):
            return False

    safe_title = re.sub(r"[^a-zA-Z0-9_-]+", "_", meta.get("title", "document"))[:80]
    out = out_dir / f"{h}_{safe_title}.txt"
    out.write_text(text)
    return True

def main():
    done = 0

    for f in APPROVED.glob("*.json"):
        meta = json.loads(f.read_text())
        url = meta["url"]

        uh = url_hash(url)
        marker = CLASSIFIED / f".done_{uh}"
        if marker.exists():
            f.unlink()
            continue

        meta = json.loads(f.read_text())
        url = meta["url"]

        uh = url_hash(url)
        marker = CLASSIFIED / f".done_{uh}"
        if marker.exists():
            f.unlink()
            continue

        meta = json.loads(f.read_text())
        url = meta["url"]
        typ = meta.get("type", "web")

        if typ == "youtube":
            text = process_youtube(url, CLASSIFIED / "youtube")
            category = "youtube"
        else:
            text = clean_html(url)
            category = "web"

        if save_text(text, meta, category):
            marker.touch()

            marker.touch()

            done += 1

        f.unlink()

    if done > 0:
        subprocess.run([
            "/openclaw/venvs/api/bin/python",
            "/openclaw/workspace/main/rag_store/build_vector_index.py"
        ])

    print(f"Processed approved: {done}")

if __name__ == "__main__":
    main()
