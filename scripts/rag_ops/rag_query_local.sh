#!/usr/bin/env bash
set -euo pipefail

SCRIPT="rag_query_local.sh"
MODE="authorized"
LOG_DIR="/openclaw/workspace/main/logs/rag_ops"
LOG_FILE="$LOG_DIR/$(date +%F_%H%M%S)_${SCRIPT}.log"
API_FILE="/openclaw/api_rag_v2.py"
URL_BASE="http://127.0.0.1:5001/rag-ask"
MAX_TIME="300"
PYTHON_BIN="/openclaw/venvs/litellm/bin/python"

QUERY="${*:-}"

mkdir -p "$LOG_DIR"

sanitize() {
  sed -E 's/token=[^& ]+/token=<REDACTED>/g'
}

urlencode() {
  QUERY_TO_ENCODE="$1" "$PYTHON_BIN" - <<'PY'
import os
from urllib.parse import quote
print(quote(os.environ.get("QUERY_TO_ENCODE", "")))
PY
}

run_check() {
  echo "STATUS=START"
  echo "SCRIPT=$SCRIPT"
  echo "MODE=$MODE"
  echo "TIMESTAMP=$(date -Is)"

  if [[ -z "$QUERY" ]]; then
    echo "STATUS=ERROR"
    echo "ERROR=query_required"
    echo "RESULT=rag_query_not_run"
    echo "NEXT=Pass a query argument."
    return 1
  fi

  if [ ! -x "$PYTHON_BIN" ]; then
    echo "STATUS=ERROR"
    echo "ERROR=python_bin_not_found"
    echo "RESULT=rag_query_not_run"
    echo "NEXT=Verify venv path."
    return 1
  fi

  if [ ! -f "$API_FILE" ]; then
    echo "STATUS=ERROR"
    echo "ERROR=api_file_not_found"
    echo "RESULT=rag_query_not_run"
    echo "NEXT=Verify api_rag_v2.py path."
    return 1
  fi

  TOKEN=$(grep -oP 'API_TOKEN\s*=\s*"\K[^"]+' "$API_FILE" || true)
  if [[ -z "$TOKEN" ]]; then
    echo "STATUS=ERROR"
    echo "ERROR=token_not_found"
    echo "RESULT=rag_query_not_run"
    echo "NEXT=Verify API_TOKEN is configured without printing it."
    return 1
  fi

  ENCODED_QUERY=$(urlencode "$QUERY")

  if [[ -z "$ENCODED_QUERY" ]]; then
    echo "STATUS=ERROR"
    echo "ERROR=query_encoding_failed"
    echo "RESULT=rag_query_not_run"
    echo "NEXT=Check query encoding function."
    return 1
  fi

  echo "QUERY=$QUERY"
  echo "URL=$URL_BASE?q=$ENCODED_QUERY&token=<REDACTED>"
  echo "--- RESPONSE_JSON ---"

  RESPONSE=$(curl --max-time "$MAX_TIME" -sS "$URL_BASE?q=$ENCODED_QUERY&token=$TOKEN")
  printf '%s\n' "$RESPONSE" | sanitize

  echo "STATUS=OK"
  echo "RESULT=rag_query_completed"
  echo "NEXT=Review answer quality and sources. Token was not printed."
}

run_check | tee "$LOG_FILE"
