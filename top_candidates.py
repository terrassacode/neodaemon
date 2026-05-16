import json
from pathlib import Path

C = Path("/openclaw/workspace/main/rag_store/candidates")

items = []

for f in C.glob("*.json"):
    try:
        d = json.loads(f.read_text(encoding="utf-8"))
        items.append(d)
    except:
        continue

items = sorted(items, key=lambda x: x.get("rank_score", 0), reverse=True)

print("\nTOP CANDIDATES:\n")

for i, d in enumerate(items[:10], start=1):
    print(f"{i}. {d.get('title', 'sin título')}")
    print(f"   score: {d.get('rank_score', 0)} | type: {d.get('type', 'unknown')} | source_type: {d.get('source_type', 'n/a')} | priority: {d.get('priority', 'n/a')}")
    print(f"   category: {d.get('category', 'n/a')} | recommendation: {d.get('recommendation', 'n/a')}")
    if d.get("review_required"):
        print("   ⚠ review_required: true")
    reasons = d.get("score_reasons", [])
    if reasons:
        print(f"   reasons: {', '.join(reasons)}")
    print(f"   url: {d.get('url', '')}\n")
