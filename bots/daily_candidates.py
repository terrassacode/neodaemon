import datetime
import feedparser
import json
from pathlib import Path

OUT = Path("/openclaw/workspace/main/rag_store/candidates")

FEEDS = [
    "https://devblogs.microsoft.com/azure-sql/feed/",
    "https://devblogs.microsoft.com/powerplatform/feed/",
    "https://community.fabric.microsoft.com/oxcrx34285/rss/board?board.id=fbc_pbiupdatesblog",

    "https://www.youtube.com/feeds/videos.xml?channel_id=UChwXzyfZXD9cD7WSRS6flsA",
    "https://www.youtube.com/feeds/videos.xml?channel_id=UC0B1xUuX5tVbZcW9o9C6P6A",
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCJd9G3pCzR0d3fX6V1r0F5Q",
    "https://www.youtube.com/feeds/videos.xml?channel_id=UCJtUOos_MwJa_Ewii-R3cJA",
    "https://www.youtube.com/feeds/videos.xml?channel_id=UC0VYwQmXx2pL8g0uF6p6S9A"
]

MAX_DAYS = 90

CONFIG_PATH = "/openclaw/config/whitelist_sources.json"
with open(CONFIG_PATH) as f:
    WHITELIST = json.load(f)



def rank_candidate(title, url, published):
    score = 0
    t = (title + " " + url).lower()

    # Fuente oficial / Microsoft
    if "microsoft.com" in t or "learn.microsoft.com" in t:
        score += 30

    # Temas prioritarios
    keywords = [
        ("fabric", 15),
        ("power bi", 15),
        ("lakehouse", 12),
        ("warehouse", 12),
        ("onelake", 12),
        ("dax", 12),
        ("semantic model", 12),
        ("mcp", 10),
        ("agent", 8),
        ("ai", 6),
        ("sql", 6),
        ("embedding", 6)
    ]

    for k, w in keywords:
        if k in t:
            score += w

    # Recencia
    try:
        age_days = (datetime.datetime.now() - published).days
        if age_days <= 7:
            score += 25
        elif age_days <= 30:
            score += 15
        elif age_days <= 90:
            score += 5
    except:
        pass

    
    # boost por tipo de contenido (features / releases)
    release_terms = [
        "feature summary", "preview", "generally available",
        "ga", "release", "update", "new", "api"
    ]

    for term in release_terms:
        if term in t:
            score += 10

    return min(score, 100)


def is_recent(entry):
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        dt = datetime.datetime(*entry.published_parsed[:6])
        return (datetime.datetime.now() - dt).days <= MAX_DAYS
    return False

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    added = 0

    for f in FEEDS:
        feed = feedparser.parse(f)

        print(f"\nFEED: {f}")
        print(f"Entries: {len(feed.entries)}")

        for e in feed.entries[:5]:
            if not is_recent(e):
                continue

            url = e.link
            name = url.replace("https://","").replace("/","_")[:80]
            path = OUT / f"{datetime.date.today()}_{name}.json"

            if path.exists():
                continue

            published_dt = datetime.datetime(*e.published_parsed[:6])

            data = {
                "url": url,
                "title": e.get("title", ""),
                "published": str(published_dt),
                "status": "candidate",
                "date_status": "valid",
                "type": "youtube" if "youtube.com" in url else "web",
                "rank_score": rank_candidate(e.get("title", ""), url, published_dt)
            }

            domain = url.split("/")[2]

            if domain in WHITELIST["blocked_domains"]:
                continue

            if domain in WHITELIST["auto_approve_domains"] and data["rank_score"] >= 60:
                out = Path("/openclaw/workspace/main/rag_store/approved") / path.name
                out.write_text(json.dumps(data, indent=2))
            else:
                path.write_text(json.dumps(data, indent=2))

            
            # filtro extra para YouTube (evitar ruido)
            if data["type"] == "youtube":
                yt_keywords = ["fabric", "lakehouse", "power bi", "dax", "semantic model"]
                title_lower = data["title"].lower()

                if not any(k in title_lower for k in yt_keywords):
                    continue

            added += 1

    print(f"\nCandidates added: {added}")

if __name__ == "__main__":
    main()