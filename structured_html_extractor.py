import json
import re
import urllib.request
from pathlib import Path
from bs4 import BeautifulSoup

APPROVED = Path("/openclaw/workspace/main/rag_store/approved")
OUT = Path("/openclaw/workspace/main/rag_store/structured")
RAW = Path("/openclaw/workspace/main/rag_store/raw_html")
LOG = Path("/openclaw/workspace/main/logs/rag_web/structured_extract.log")

OUT.mkdir(parents=True, exist_ok=True)
RAW.mkdir(parents=True, exist_ok=True)
LOG.parent.mkdir(parents=True, exist_ok=True)

REMOVE_TAGS = ["script", "style", "nav", "footer", "header", "aside", "form"]

def log(msg):
    with LOG.open("a", encoding="utf-8") as f:
        f.write(msg + "\n")

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", errors="ignore")

def clean_spaces(text):
    return re.sub(r"\s+", " ", text).strip()


def extract_blocks(html):
    soup = BeautifulSoup(html, "lxml")

    for tag in soup(REMOVE_TAGS):
        tag.decompose()

    # fallback multi-dominio (community incluido)
    main = (
        soup.find("div", {"class": "lia-message-body-content"})
        or soup.find("div", {"class": "lia-message-body"})
        or soup.find("main")
        or soup.find("article")
        or soup.body
    )

    blocks = []

    if not main:
        return blocks

    for el in main.find_all(["h1", "h2", "h3", "p", "li", "pre", "code"], recursive=True):
        name = el.name

        if name in ["pre", "code"]:
            text = el.get_text("\n", strip=False).strip()
            if len(text) > 20:
                blocks.append({
                    "type": "code",
                    "tag": name,
                    "language": "unknown",
                    "content": text
                })
            continue

        text = clean_spaces(el.get_text(" ", strip=True))

        if len(text) < 30:
            continue

        if name in ["h1", "h2", "h3"]:
            btype = "heading"
        elif name == "li":
            btype = "list_item"
        else:
            btype = "paragraph"

        blocks.append({
            "type": btype,
            "tag": name,
            "content": text
        })

    return blocks
def quality_score(blocks):
    if not blocks:
        return 0

    score = 0

    text_blocks = [b for b in blocks if b["type"] in ["paragraph", "list_item"]]
    code_blocks = [b for b in blocks if b["type"] == "code"]
    headings = [b for b in blocks if b["type"] == "heading"]

    if len(text_blocks) >= 3:
        score += 30
    if headings:
        score += 20
    if code_blocks:
        score += 20

    total_chars = sum(len(b["content"]) for b in blocks)
    if total_chars > 1000:
        score += 20
    if total_chars > 3000:
        score += 10

    return min(score, 100)

created = 0

for f in APPROVED.glob("*.json"):
    try:
        d = json.loads(f.read_text(encoding="utf-8"))
        url = d.get("url")

        if not url:
            continue

        print(f"Extrayendo estructurado: {d.get('title')}")
        html = fetch(url)

        raw_file = RAW / f"{f.stem}.html"
        raw_file.write_text(html, encoding="utf-8")

        blocks = extract_blocks(html)
        q = quality_score(blocks)

        out = {
            "title": d.get("title"),
            "url": url,
            "source_type": d.get("source_type"),
            "category": d.get("category"),
            "rank_score": d.get("rank_score"),
            "status": "structured_html",
            "quality_score": q,
            "blocks_count": len(blocks),
            "blocks": blocks
        }

        out_file = OUT / f.name
        out_file.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

        log(f"STRUCTURED file={f.name} quality={q} blocks={len(blocks)} url={url}")
        created += 1

    except Exception as e:
        log(f"ERROR file={f.name} error={e}")

print(f"Estructurados: {created}")
