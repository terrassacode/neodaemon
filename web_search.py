import json
import time
import hashlib
import urllib.parse
import urllib.request
from pathlib import Path

BASE = Path("/openclaw/workspace/main/rag_store")
OUT = BASE / "candidates"
OUT.mkdir(parents=True, exist_ok=True)

LOG = Path("/openclaw/workspace/main/logs/rag_web/search.log")
LOG.parent.mkdir(parents=True, exist_ok=True)

DOMAINS = [
    "learn.microsoft.com",
    "community.fabric.microsoft.com",
    "blog.fabric.microsoft.com",
    "devblogs.microsoft.com",
    "powerbi.microsoft.com"
]

QUERIES = [
    "Microsoft Fabric updates",
    "Fabric Lakehouse Warehouse differences",
    "Power BI Fabric semantic model",
    "Microsoft Fabric Real-Time Intelligence",
]

# -------- utils --------

def log(msg):
    LOG.write_text(
        (LOG.read_text() if LOG.exists() else "") +
        f"{time.strftime('%Y-%m-%d %H:%M:%S')} {msg}\n"
    )

def hash_url(url):
    return hashlib.md5(url.encode()).hexdigest()

def already_exists(url_hash):
    for f in OUT.glob("*.json"):
        try:
            data = json.loads(f.read_text())
            if data.get("id") == url_hash:
                return True
        except:
            continue
    return False

def allowed(url):
    return any(d in url.lower() for d in DOMAINS)

# -------- search --------

def duckduckgo_html(query):
    url = "https://html.duckduckgo.com/html/?" + urllib.parse.urlencode({"q": query})
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8", errors="ignore")

def extract_links(html):
    links = []
    marker = 'class="result__a" href="'
    for part in html.split(marker)[1:]:
        raw = part.split('"', 1)[0]
        raw = raw.replace("&amp;", "&")

        if "uddg=" in raw:
            qs = urllib.parse.parse_qs(urllib.parse.urlparse(raw).query)
            url = qs.get("uddg", [raw])[0]
        else:
            url = raw

        links.append(url)
    return links

# -------- scoring --------

def score_url(url):
    u = url.lower()
    score = 0
    reasons = []

    if "fabric" in u:
        score += 40; reasons.append("fabric_keyword")

    if "powerbi" in u or "power-bi" in u:
        score += 20; reasons.append("powerbi_keyword")

    if "learn.microsoft.com" in u:
        score += 30; reasons.append("official_docs")

    if "community.fabric.microsoft.com" in u:
        score += 25; reasons.append("community")

    if "blog.fabric.microsoft.com" in u:
        score += 25; reasons.append("official_blog")

    if "devblogs.microsoft.com" in u:
        score += 15; reasons.append("dev_blog")

    if "update" in u or "preview" in u:
        score += 10; reasons.append("fresh_signal")

    return score, reasons

def classify(url):
    u = url.lower()

    if "learn.microsoft.com" in u:
        return "docs"
    if "community.fabric.microsoft.com" in u:
        return "community"
    if "blog.fabric.microsoft.com" in u:
        return "blog"
    if "devblogs.microsoft.com" in u:
        return "devblog"

    return "web"

# -------- main --------

created = 0

for query in QUERIES:
    log(f"QUERY: {query}")

    try:
        html = duckduckgo_html(query)
        links = extract_links(html)

        for url in links:
            if not allowed(url):
                continue

            url_hash = hash_url(url)

            if already_exists(url_hash):
                continue

            score, reasons = score_url(url)

            if score < 30:
                continue

            doc = {
                "id": url_hash,
                "url": url,
                "title": url.split("/")[-1][:120],
                "query": query,
                "source": "internet",
                "type": classify(url),
                "domain": "fabric",
                "rank_score": score,
                "score_reasons": reasons,
                "status": "candidate",
                "captured_at": time.strftime("%Y-%m-%dT%H:%M:%S")
            }

            file = OUT / f"{url_hash}.json"
            file.write_text(json.dumps(doc, indent=2, ensure_ascii=False))

            log(f"CREATED: {url} score={score}")
            created += 1

    except Exception as e:
        log(f"ERROR query={query} error={e}")

print(f"Candidatos creados: {created}")
