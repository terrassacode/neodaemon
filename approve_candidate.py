import json
import shutil
import sys
from pathlib import Path

C = Path("/openclaw/workspace/main/rag_store/candidates")
A = Path("/openclaw/workspace/main/rag_store/approved")
A.mkdir(parents=True, exist_ok=True)

# cargar candidatos ordenados igual que /top
items = []
files = []

for f in C.glob("*.json"):
    try:
        d = json.loads(f.read_text(encoding="utf-8"))
        items.append(d)
        files.append(f)
    except:
        continue

# ordenar por score
combined = list(zip(items, files))
combined.sort(key=lambda x: x[0].get("rank_score", 0), reverse=True)

if len(sys.argv) < 2:
    print("Uso: python3 approve_candidate.py <index>")
    sys.exit(1)

idx = int(sys.argv[1]) - 1

if idx < 0 or idx >= len(combined):
    print("Índice inválido")
    sys.exit(1)

data, file_path = combined[idx]

# actualizar estado
data["status"] = "approved"

# guardar antes de mover
file_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

target = A / file_path.name
shutil.move(str(file_path), str(target))

print(f"✔ Approved y movido:")
print(f"{data.get('title')}")
print(f"{data.get('url')}")
