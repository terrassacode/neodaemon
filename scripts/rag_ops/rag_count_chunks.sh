#!/usr/bin/env bash
set -euo pipefail

SCRIPT="rag_count_chunks.sh"
MODE="readonly"
LOG_DIR="/openclaw/workspace/main/logs/rag_ops"
LOG_FILE="$LOG_DIR/$(date +%F_%H%M%S)_${SCRIPT}.log"
CHUNKS_DIR="/openclaw/workspace/main/rag_store/chunks_v2"
SHOW_LIST="false"

if [[ "${1:-}" == "--list" || "${1:-}" == "--verbose" ]]; then
  SHOW_LIST="true"
fi

mkdir -p "$LOG_DIR"

run_check() {
  echo "STATUS=START"
  echo "SCRIPT=$SCRIPT"
  echo "MODE=$MODE"
  echo "CHUNKS_DIR=$CHUNKS_DIR"
  echo "TIMESTAMP=$(date -Is)"

  if [ ! -d "$CHUNKS_DIR" ]; then
    echo "STATUS=ERROR"
    echo "ERROR=chunks_dir_not_found"
    echo "RESULT=chunk_count_0"
    echo "NEXT=Verify RAG chunks directory path."
    return 1
  fi

  COUNT=$(find "$CHUNKS_DIR" -maxdepth 1 -type f -name '*.json' | wc -l | tr -d ' ')

  echo "STATUS=OK"
  echo "RESULT=chunk_count_$COUNT"

  if [[ "$SHOW_LIST" == "true" ]]; then
    echo "--- CHUNK_FILES ---"
    find "$CHUNKS_DIR" -maxdepth 1 -type f -name '*.json' -printf '%f\n' | sort
  fi

  echo "NEXT=Use --list only when file names are needed."
}

run_check | tee "$LOG_FILE"
