#!/usr/bin/env bash
set -euo pipefail

SCRIPT="rag_status_readonly.sh"
MODE="readonly"
LOG_DIR="/openclaw/workspace/main/logs/rag_ops"
LOG_FILE="$LOG_DIR/$(date +%F_%H%M%S)_${SCRIPT}.log"
SERVICE="openclaw-rag-v2.service"
VERBOSE="false"

if [[ "${1:-}" == "--verbose" ]]; then
  VERBOSE="true"
fi

mkdir -p "$LOG_DIR"

sanitize() {
  sed -E 's/token=[^& ]+/token=<REDACTED>/g'
}

run_check() {
  echo "STATUS=START"
  echo "SCRIPT=$SCRIPT"
  echo "MODE=$MODE"
  echo "SERVICE=$SERVICE"
  echo "TIMESTAMP=$(date -Is)"

  ACTIVE_STATE=$(systemctl --user is-active "$SERVICE" 2>/dev/null || true)
  LOAD_STATE=$(systemctl --user show "$SERVICE" --property=LoadState --value 2>/dev/null || true)
  SUB_STATE=$(systemctl --user show "$SERVICE" --property=SubState --value 2>/dev/null || true)
  MAIN_PID=$(systemctl --user show "$SERVICE" --property=MainPID --value 2>/dev/null || true)

  echo "SERVICE_ACTIVE=${ACTIVE_STATE:-unknown}"
  echo "SERVICE_LOAD=${LOAD_STATE:-unknown}"
  echo "SERVICE_SUBSTATE=${SUB_STATE:-unknown}"
  echo "SERVICE_MAINPID=${MAIN_PID:-unknown}"

  RECENT_ERRORS=$(journalctl --user -u "$SERVICE" -n 80 --no-pager 2>/dev/null | grep -Ei "error|failed|traceback|exception|brokenpipe" | sanitize | tail -n 10 || true)
  if [[ -n "$RECENT_ERRORS" ]]; then
    echo "RECENT_ERRORS=present"
    echo "--- RECENT_ERRORS_LAST_10_SANITIZED ---"
    echo "$RECENT_ERRORS"
  else
    echo "RECENT_ERRORS=none"
  fi

  if [[ "$VERBOSE" == "true" ]]; then
    echo "--- STATUS_VERBOSE_SANITIZED ---"
    systemctl --user status "$SERVICE" --no-pager | sanitize || true
    echo "--- JOURNAL_LAST_80_SANITIZED ---"
    journalctl --user -u "$SERVICE" -n 80 --no-pager | sanitize || true
  fi

  if [[ "$ACTIVE_STATE" == "active" ]]; then
    echo "STATUS=OK"
    echo "RESULT=service_active"
  else
    echo "STATUS=ERROR"
    echo "RESULT=service_not_active"
  fi

  echo "NEXT=Use --verbose only when sanitized full logs are needed. No changes were made."
}

run_check | tee "$LOG_FILE"
