#!/bin/bash

SOURCE=${1:-"unknown"}
ACTION="openclaw_$SOURCE"

START=$(date +%s%3N)

/openclaw/logs/new_task.sh >/dev/null

cleanup() {
  END=$(date +%s%3N)
  DURATION=$((END - START))

  if [ -z "$STATUS_CODE" ]; then
    STATUS="interrupted"
  elif [ $STATUS_CODE -eq 0 ]; then
    STATUS="success"
  else
    STATUS="fail"
  fi

  /openclaw/logs/log_event_v2.sh "$SOURCE" "${ACTION}_end" "$STATUS" "low" "$DURATION"
}

trap cleanup EXIT

/openclaw/logs/log_event_v2.sh "$SOURCE" "${ACTION}_start" "success" "low" 0

openclaw "$SOURCE"
STATUS_CODE=$?

exit $STATUS_CODE
