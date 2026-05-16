import json
import re
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

APPROVED = Path("/openclaw/workspace/main/rag_store/approved")
PROCESSED = Path("/openclaw/workspace/main/rag_store/processed")
LOG = Path("/openclaw/workspace/main/logs/rag_web/process.log")

PROCESSED.mkdir(parents=True, exist_ok=True)
LOG.parent.mkdir(parents=True, exist_ok=True)

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip = False
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in ["script", "style", "nav", "footer", "header", "aside"]:
            self.skip = True

    def handle_endtag(self, tag):
        if tag in ["script", "style", "nav", "footer", "header", "aside"]:
            self.skip = False

    def handle_data(self, data):
        if not self.skip:
            text = data.strip()
            if text:
                self.parts.append(text)

def clean_text(text):
    noise_phrases = [
        "skip to main content",
        "A new Data Days event is coming soon",
        "Register · Sign in · Help",
        "Go To Updates blog",
        "Fabric Updates Blog",
        "Power BI Updates Blog",
        "All community Blog",
        "Knowledge base",
        "Turn on suggestions",
        "Auto-suggest helps you quickly narrow down your search results",
        "Showing results for",
        "Search instead for",
        "Did you mean",
        "Did you hear",
        "Start preparing now",
        "Register now",
        "Article Options",
        "Subscribe to RSS Feed",
        "Mark as New",
        "Mark as Read",
        "Bookmark",
        "Subscribe",
        "Print",
        "Report Inappropriate Content",
    ]

    for phrase in noise_phrases:
        text = text.replace(phrase, " ")

    # recorte fuerte para páginas community
    markers_start = [
        "Execute DAX Queries REST API (Preview)",
    ]
    for m in markers_start:
        pos = text.find(m)
        if pos != -1:
            text = text[pos:]
            break

    markers_end = [
        "Labels:",
        "Message 1 of",
        "Comments",
        "You must be a registered user",
    ]
    for m in markers_end:
        pos = text.find(m)
        if pos != -1:
            text = text[:pos]
            break

    # para blogs Community, empezar desde Author si existe
    pos = text.find("Author:")
    if pos != -1:
        text = text[pos:]

    text = re.sub(r"\s+", " ", text)
    return text.strip()

def fetch(url):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", errors="ignore")

def log(msg):
    with LOG.open("a", encoding="utf-8") as f:
        f.write(msg + "\n")

processed = 0

for f in APPROVED.glob("*.json"):
    try:
        d = json.loads(f.read_text(encoding="utf-8"))

        if d.get("status") == "processed":
            continue

        url = d.get("url")
        if not url:
            continue

        print(f"Procesando: {d.get('title')}")
        html = fetch(url)

        parser = TextExtractor()
        parser.feed(html)

        text = clean_text(" ".join(parser.parts))

        if len(text) < 500:
            log(f"SKIP short_text file={f.name} url={url}")
            continue

        out = {
            "title": d.get("title"),
            "url": url,
            "source_type": d.get("source_type"),
            "category": d.get("category"),
            "rank_score": d.get("rank_score"),
            "status": "processed_text",
            "text": text[:50000]
        }

        out_file = PROCESSED / f.name
        out_file.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

        d["status"] = "processed"
        f.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")

        log(f"PROCESSED file={f.name} chars={len(text)} url={url}")
        processed += 1

    except Exception as e:
        log(f"ERROR file={f.name} error={e}")

print(f"Procesados: {processed}")
