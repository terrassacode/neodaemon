#!/usr/bin/env bash
set -euo pipefail

SCRIPT="rag_py_compile.sh"
MODE="validation"
LOG_DIR="/openclaw/workspace/main/logs/rag_ops"
LOG_FILE="$LOG_DIR/$(date +%F_%H%M%S)_${SCRIPT}.log"
TARGET="/openclaw/api_rag_v2.py"

mkdir -p "$LOG_DIR"

run_check() {
  echo "STATUS=START"
  echo "SCRIPT=$SCRIPT"
  echo "MODE=$MODE"
  echo "TARGET=$TARGET"
  echo "TIMESTAMP=$(date -Is)"

  if [ ! -f "$TARGET" ]; then
    echo "STATUS=ERROR"
    echo "ERROR=target_not_found"
    echo "RESULT=py_compile_not_run"
    echo "NEXT=Verify api_rag_v2.py path."
    return 1
  fi

  if timeout 30s python3 -m py_compile "$TARGET"; then
    echo "STATUS=OK"
    echo "RESULT=py_compile_ok"
    echo "NEXT=Safe to continue validation. No changes were made."
  else
    echo "STATUS=ERROR"
    echo "RESULT=py_compile_failed"
    echo "NEXT=Do not restart service. Inspect syntax error and rollback if needed."
    return 1
  fi
}

run_check | tee "$LOG_FILE"
