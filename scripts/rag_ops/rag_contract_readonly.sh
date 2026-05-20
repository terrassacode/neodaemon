#!/usr/bin/env bash
set -euo pipefail

SCRIPT="rag_contract_readonly.sh"
MODE="readonly_contract_inspection"

FILES=(
  "/openclaw/rag_loader.py"
  "/openclaw/rag_retriever.py"
  "/openclaw/rag_filter.py"
  "/openclaw/api_rag_v2.py"
)

PATTERN='chunks_v2|rag_store|load_chunks|retrieve_chunks|filter_results|json|glob|open\(|Path|CHUNK|chunk|text|content|chunk_id|url|source|title|quality_score|keywords|query_patterns|validation|status|applicability|risk_note|cache|lru|global'

sanitize() {
  sed -E \
    -e 's/(token|api[_-]?key|secret|password|authorization|bearer)[[:space:]]*[:=][[:space:]]*["'"'"']?[^"'"'"'[:space:]]+/\1=<REDACTED>/Ig' \
    -e 's/(Bearer )[A-Za-z0-9._~+\/=-]+/\1<REDACTED>/Ig'
}

echo "STATUS=START"
echo "SCRIPT=$SCRIPT"
echo "MODE=$MODE"
echo "FILES_ALLOWED=${FILES[*]}"
echo "PATTERN=$PATTERN"

for f in "${FILES[@]}"; do
  echo "--- FILE=$f ---"

  if [ ! -f "$f" ]; then
    echo "FILE_STATUS=missing"
    continue
  fi

  echo "FILE_STATUS=present"
  grep -nE "$PATTERN" "$f" 2>/dev/null | sanitize || true
done

echo "STATUS=OK"
echo "RESULT=readonly_contract_inspection_completed"
echo "NEXT=Review loader folder, text/content handling, metadata usage, cache/restart behavior."
