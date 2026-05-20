#!/usr/bin/env bash
set -euo pipefail

SCRIPT="rag_count_chunks.sh"
MODE="readonly"
LOG_DIR="/openclaw/workspace/main/logs/rag_ops"
LOG_FILE="$LOG_DIR/$(date +%F_%H%M%S)_${SCRIPT}.log"
CHUNKS_DIR="/openclaw/workspace/main/rag_store/chunks_v2"

mkdir -p "$LOG_DIR"

{
  echo "STATUS=START"
  echo "SCRIPT=$SCRIPT"
  echo "MODE=$MODE"
  echo "CHUNKS_DIR=$CHUNKS_DIR"
  echo "TIMESTAMP=$(date -Is)"

  if [ ! -d "$CHUNKS_DIR" ]; then
    echo "STATUS=ERROR"
    echo "ERROR=chunks_dir_not_found"
    echo "RESULT=0"
    echo "NEXT=Verify RAG chunks directory path."
    exit 1
  fi

  COUNT=$(find "$CHUNKS_DIR" -maxdepth 1 -type f -name '*.json' | wc -l | tr -d ' ')

  echo "STATUS=OK"
  echo "RESULT=chunk_count_$COUNT"
  echo "--- CHUNK_FILES ---"
  find "$CHUNKS_DIR" -maxdepth 1 -type f -name '*.json' -printf '%f\n' | sort
  echo "NEXT=Use rag_test_bm25.sh in F2 after read-only wrappers are validated."
} | tee "$LOG_FILE"
