#!/usr/bin/env bash
set -euo pipefail

SCRIPT="rag_status_readonly.sh"
MODE="readonly"
LOG_DIR="/openclaw/workspace/main/logs/rag_ops"
LOG_FILE="$LOG_DIR/$(date +%F_%H%M%S)_${SCRIPT}.log"
SERVICE="openclaw-rag-v2.service"

mkdir -p "$LOG_DIR"

{
  echo "STATUS=START"
  echo "SCRIPT=$SCRIPT"
  echo "MODE=$MODE"
  echo "SERVICE=$SERVICE"
  echo "TIMESTAMP=$(date -Is)"
  echo "--- STATUS ---"

  if systemctl --user status "$SERVICE" --no-pager; then
    STATUS_RESULT="service_status_ok"
  else
    STATUS_RESULT="service_status_error"
  fi

  echo "--- JOURNAL_LAST_80 ---"
  journalctl --user -u "$SERVICE" -n 80 --no-pager || true

  echo "STATUS=OK"
  echo "RESULT=$STATUS_RESULT"
  echo "NEXT=Review service status and logs. No changes were made."
} | tee "$LOG_FILE"
