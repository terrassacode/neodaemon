#!/usr/bin/env bash
set -euo pipefail

SCRIPT="rag_test_bm25.sh"
MODE="validation"
LOG_DIR="/openclaw/workspace/main/logs/rag_ops"
LOG_FILE="$LOG_DIR/$(date +%F_%H%M%S)_${SCRIPT}.log"
PYTHON_BIN="/openclaw/venvs/litellm/bin/python"
OPENCLAW_DIR="/openclaw"
DEFAULT_QUERY="baseline std_RD_actual std_RD_baseline RobotId ProgramId ID_SW media global inestabilidad"
QUERY="${*:-$DEFAULT_QUERY}"

mkdir -p "$LOG_DIR"

run_check() {
  echo "STATUS=START"
  echo "SCRIPT=$SCRIPT"
  echo "MODE=$MODE"
  echo "TIMESTAMP=$(date -Is)"
  echo "QUERY=$QUERY"

  if [ ! -x "$PYTHON_BIN" ]; then
    echo "STATUS=ERROR"
    echo "ERROR=python_bin_not_found"
    echo "RESULT=bm25_not_run"
    echo "NEXT=Verify venv path."
    return 1
  fi

  cd "$OPENCLAW_DIR"

  QUERY_ENV="$QUERY" timeout 60s "$PYTHON_BIN" - <<'PY'
import os
from rag_loader import load_chunks
from rag_retriever import retrieve_chunks
from rag_filter import filter_results

q = os.environ.get("QUERY_ENV", "")
chunks = load_chunks()
results = filter_results(retrieve_chunks(chunks, q, top_k=5))

print(f"CHUNKS_LOADED={len(chunks)}")
print(f"RESULTS_RETURNED={len(results)}")
for idx, r in enumerate(results[:5], 1):
    print(f"RESULT_{idx}_SCORE={r.get('score')}")
    print(f"RESULT_{idx}_CHUNK_ID={r.get('chunk_id')}")
    print(f"RESULT_{idx}_URL={r.get('url')}")
PY

  echo "STATUS=OK"
  echo "RESULT=bm25_test_completed"
  echo "NEXT=Review top chunk_id and score. No Ollama, no token, no /rag-ask used."
}

run_check | tee "$LOG_FILE"
