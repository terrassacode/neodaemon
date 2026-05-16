import json
from pathlib import Path

C = Path("/openclaw/workspace/main/rag_store/candidates")

def classify(d):
    url = d.get("url", "").lower()
    title = d.get("title", "").lower()
    typ = d.get("type", "").lower()
    score = int(d.get("rank_score", 0))

    text = f"{title} {url}"

    category = "general"
    source_type = "web"
    priority = "medium"
    review_required = True
    recommendation = "review"

    if "learn.microsoft.com" in url:
        source_type = "official_docs"
        priority = "high"
        review_required = False
        recommendation = "approve_candidate"

    elif "community.fabric.microsoft.com" in url:
        source_type = "community_blog"
        priority = "high" if score >= 80 else "medium"
        review_required = True
        recommendation = "review_high_value" if score >= 80 else "review"

    elif "blog.fabric.microsoft.com" in url:
        source_type = "official_blog"
        priority = "high"
        review_required = True
        recommendation = "review_high_value"

    elif "devblogs.microsoft.com" in url:
        source_type = "dev_blog"
        priority = "medium"
        review_required = True
        recommendation = "review"

    elif typ == "youtube" or "youtube.com" in url:
        source_type = "video"
        priority = "low"
        review_required = True
        recommendation = "manual_review_only"

    if "semantic" in text or "model" in text:
        category = "semantic_model"
    elif "lakehouse" in text or "warehouse" in text:
        category = "lakehouse_warehouse"
    elif "real-time" in text or "realtime" in text or "real-time-intelligence" in text:
        category = "real_time_intelligence"
    elif "dataflow" in text:
        category = "dataflows"
    elif "dax" in text:
        category = "dax"
    elif "translytical" in text:
        category = "translytical"

    return category, source_type, priority, review_required, recommendation

updated = 0

for f in C.glob("*.json"):
    try:
        d = json.loads(f.read_text(encoding="utf-8"))
        category, source_type, priority, review_required, recommendation = classify(d)

        d["category"] = category
        d["source_type"] = source_type
        d["priority"] = priority
        d["review_required"] = review_required
        d["recommendation"] = recommendation

        f.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
        updated += 1
    except Exception as e:
        print(f"ERROR {f}: {e}")

print(f"Clasificados: {updated}")
