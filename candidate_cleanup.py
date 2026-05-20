import json, shutil
from pathlib import Path

C = Path("/openclaw/workspace/main/rag_store/candidates")
Q = Path("/openclaw/workspace/main/rag_store/quarantine")
Q.mkdir(parents=True, exist_ok=True)

moved = 0
kept = 0

def should_quarantine(d):
    url = d.get("url", "").lower()
    title = d.get("title", "").lower()
    typ = d.get("type", "").lower()
    score = int(d.get("rank_score", 0))

    if typ == "youtube" and not ("fabric" in title and score >= 50):
        return True, "youtube_low_relevance"

    if "powerplatform" in url and "fabric" not in title:
        return True, "powerplatform_not_fabric_core"

    if "azure-sql" in url and "fabric" not in title:
        return True, "azure_sql_not_fabric_core"

    if "excel" in title and "fabric" not in title:
        return True, "excel_not_fabric_core"

    return False, ""

for f in C.glob("*.json"):
    try:
        d = json.loads(f.read_text(encoding="utf-8"))
        quarantine, reason = should_quarantine(d)

        if quarantine:
            d["status"] = "quarantine"
            d["quarantine_reason"] = reason
            target = Q / f.name
            f.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
            shutil.move(str(f), str(target))
            moved += 1
        else:
            kept += 1

    except Exception as e:
        print(f"ERROR {f}: {e}")

print(f"Kept: {kept}")
print(f"Moved to quarantine: {moved}")
