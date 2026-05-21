#!/usr/bin/env bash
set -euo pipefail

SCRIPT="rag_query_debug_context.sh"
MODE="retrieval_only_debug"
OPENCLAW_DIR="/openclaw"
PYTHON_BIN="/openclaw/venvs/litellm/bin/python"
CHUNKS_DIR="/openclaw/workspace/main/rag_store/chunks_v2"
QUERY="${*:-}"

if [ -z "$QUERY" ]; then
  echo "STATUS=ERROR"
  echo "SCRIPT=$SCRIPT"
  echo "ERROR=missing_query"
  echo "USAGE=$SCRIPT <query>"
  exit 2
fi

echo "STATUS=START"
echo "SCRIPT=$SCRIPT"
echo "MODE=$MODE"
echo "QUERY=$QUERY"
echo "NOTE=Retrieval-only. No Ollama. No /rag-ask. No writes."

if [ ! -x "$PYTHON_BIN" ]; then
  echo "STATUS=ERROR"
  echo "ERROR=python_bin_not_found"
  echo "PYTHON_BIN=$PYTHON_BIN"
  exit 1
fi

if [ ! -d "$CHUNKS_DIR" ]; then
  echo "STATUS=ERROR"
  echo "ERROR=chunks_dir_not_found"
  echo "CHUNKS_DIR=$CHUNKS_DIR"
  exit 1
fi

cd "$OPENCLAW_DIR"

QUERY_ENV="$QUERY" CHUNKS_DIR_ENV="$CHUNKS_DIR" "$PYTHON_BIN" - <<'PY'
import json
import os
import re
from pathlib import Path

from rag_loader import load_chunks
from rag_retriever import retrieve_chunks
from rag_filter import filter_results

query = os.environ.get("QUERY_ENV", "")
chunks_dir = Path(os.environ.get("CHUNKS_DIR_ENV", "/openclaw/workspace/main/rag_store/chunks_v2"))

def one_line(value, limit=420):
    if value is None:
        return ""
    text = str(value)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:limit]

def chunk_text(item):
    for key in ("text", "content", "body", "summary"):
        value = item.get(key) if isinstance(item, dict) else None
        if isinstance(value, str) and value.strip():
            return value
    return ""

chunks = load_chunks()
results = filter_results(retrieve_chunks(chunks, query, top_k=5))

print(f"CHUNKS_LOADED={len(chunks)}")
print(f"RESULTS_RETURNED={len(results)}")

for idx, result in enumerate(results[:5], 1):
    print(f"RESULT_{idx}_SCORE={result.get('score')}")
    print(f"RESULT_{idx}_CHUNK_ID={result.get('chunk_id')}")
    print(f"RESULT_{idx}_URL={result.get('url')}")
    print(f"RESULT_{idx}_TEXT_SNIPPET={one_line(chunk_text(result))}")

terms = [
    "corrosion",
    "corrosión",
    "1.5",
    "std_RD_actual",
    "std_RD_baseline",
    "robot, robot",
]

print("SEARCH_STATUS=START")
json_files = sorted(chunks_dir.glob("*.json"))
print(f"SEARCH_FILES={len(json_files)}")

for term in terms:
    term_lower = term.lower()
    matches = []
    for path in json_files:
        try:
            raw = path.read_text(encoding="utf-8", errors="replace")
        except Exception as exc:
            matches.append((path.name, f"READ_ERROR={exc}"))
            continue
        if term_lower in raw.lower():
            snippet = one_line(raw[max(0, raw.lower().find(term_lower) - 120): raw.lower().find(term_lower) + 220])
            matches.append((path.name, snippet))
    print(f"SEARCH_TERM={term}")
    print(f"SEARCH_MATCHES={len(matches)}")
    for idx, (name, snippet) in enumerate(matches[:10], 1):
        print(f"SEARCH_{term}_MATCH_{idx}_FILE={name}")
        print(f"SEARCH_{term}_MATCH_{idx}_SNIPPET={snippet}")

print("SEARCH_STATUS=OK")
print("STATUS=OK")
print("RESULT=retrieval_debug_completed")
print("NEXT=Review retrieved chunk_ids, snippets, and search matches before changing chunks or prompt.")
PY
