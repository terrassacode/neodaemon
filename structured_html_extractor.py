from bs4 import BeautifulSoup
from pathlib import Path
import json

INPUT_DIR = "/openclaw/workspace/main/rag_store/processed"
OUTPUT_DIR = "/openclaw/workspace/main/rag_store/structured"


def extract_blocks(html):
    soup = BeautifulSoup(html, "lxml")

    # eliminar ruido
    for tag in soup(["script", "style", "nav", "footer"]):
        tag.decompose()

    main = (
        soup.find("div", {"class": "lia-message-body-content"})
        or soup.find("article")
        or soup.find("main")
        or soup.body
    )

    blocks = []
    current_section = None

    for el in main.find_all(["h1", "h2", "h3", "p", "li", "pre", "code"]):
        tag = el.name
        text = el.get_text(" ", strip=True)

        if not text:
            continue

        # headings → nueva sección
        if tag in ["h1", "h2", "h3"]:
            current_section = text
            blocks.append({
                "type": "heading",
                "content": text
            })
            continue

        # código real
        if tag == "pre":
            blocks.append({
                "type": "code",
                "section": current_section,
                "content": el.get_text("\n", strip=False)
            })
            continue

        # texto normal
        blocks.append({
            "type": "text",
            "section": current_section,
            "content": text
        })

    return blocks


def quality_score(blocks):
    if not blocks:
        return 0

    text_blocks = [b for b in blocks if b["type"] == "text"]
    code_blocks = [b for b in blocks if b["type"] == "code"]

    score = 0

    if len(text_blocks) > 5:
        score += 30
    if len(code_blocks) > 0:
        score += 30
    if len(blocks) > 10:
        score += 20

    avg_len = sum(len(b["content"]) for b in blocks) / len(blocks)
    if avg_len > 100:
        score += 20

    return score


def process():
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    files = list(Path(INPUT_DIR).glob("*.json"))

    for f in files:
        data = json.loads(f.read_text())

        html = data.get("raw_html", "")
        blocks = extract_blocks(html)
        score = quality_score(blocks)

        out = {
            "title": data.get("title"),
            "url": data.get("url"),
            "blocks": blocks,
            "quality_score": score
        }

        out_path = Path(OUTPUT_DIR) / f.name
        out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2))

        print(f"Procesado: {f.name} | score={score}")


if __name__ == "__main__":
    process()
