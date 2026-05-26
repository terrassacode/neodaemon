#!/usr/bin/env bash
set -u

# Update the static Resource Usage dashboard data.
# This wrapper does not register new events by itself.
# It only runs the exporter that reads logs/resource_usage.jsonl and writes dashboard-v2/data/resource_usage.json.

BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
EXPORT_SCRIPT="$BASE_DIR/scripts/export_resource_usage_dashboard.py"
METRICS_SCRIPT="$BASE_DIR/scripts/export_resource_usage_metrics.py"
ALERTS_SCRIPT="$BASE_DIR/scripts/check_resource_usage_alerts.py"
TOKEN_DASHBOARD_SCRIPT="$BASE_DIR/scripts/export_token_dashboard.py"
OUTPUT_PATH="$BASE_DIR/dashboard-v2/data/resource_usage.json"
METRICS_OUTPUT_PATH="$BASE_DIR/dashboard-v2/data/resource_usage_metrics.json"
TOKEN_DASHBOARD_OUTPUT_PATH="$BASE_DIR/dashboard-v2/data/token_dashboard.json"

if [ ! -f "$EXPORT_SCRIPT" ]; then
  printf 'ERROR: export script not found: %s\n' "$EXPORT_SCRIPT" >&2
  exit 1
fi

python3 "$EXPORT_SCRIPT"

if [ -f "$METRICS_SCRIPT" ]; then
  if ! python3 "$METRICS_SCRIPT"; then
    printf 'WARNING: metrics export failed: %s\n' "$METRICS_SCRIPT" >&2
  fi
else
  printf 'WARNING: metrics script not found: %s\n' "$METRICS_SCRIPT" >&2
fi

if [ -f "$ALERTS_SCRIPT" ]; then
  if ! python3 "$ALERTS_SCRIPT"; then
    printf 'WARNING: alert check failed\n' >&2
  fi
else
  printf 'WARNING: alert script not found: %s\n' "$ALERTS_SCRIPT" >&2
fi

if [ -f "$TOKEN_DASHBOARD_SCRIPT" ]; then
  if ! python3 "$TOKEN_DASHBOARD_SCRIPT"; then
    printf 'WARNING: token dashboard export failed: %s\n' "$TOKEN_DASHBOARD_SCRIPT" >&2
  fi
else
  printf 'WARNING: token dashboard script not found: %s\n' "$TOKEN_DASHBOARD_SCRIPT" >&2
fi

if [ ! -f "$OUTPUT_PATH" ]; then
  printf 'ERROR: output not generated: %s\n' "$OUTPUT_PATH" >&2
  exit 1
fi

COUNT="unknown"
GENERATED_AT="unknown"

if command -v python3 >/dev/null 2>&1; then
  COUNT="$(python3 - <<'PY' "$OUTPUT_PATH"
import json
import sys
from pathlib import Path
path = Path(sys.argv[1])
try:
    data = json.loads(path.read_text(encoding='utf-8'))
    print(data.get('count', 'unknown'))
except Exception:
    print('unknown')
PY
)"
  GENERATED_AT="$(python3 - <<'PY' "$OUTPUT_PATH"
import json
import sys
from pathlib import Path
path = Path(sys.argv[1])
try:
    data = json.loads(path.read_text(encoding='utf-8'))
    print(data.get('generated_at', 'unknown'))
except Exception:
    print('unknown')
PY
)"
fi

printf 'Resource Usage dashboard data updated\n'
printf 'output path: %s\n' "$OUTPUT_PATH"
printf 'metrics output path: %s\n' "$METRICS_OUTPUT_PATH"
printf 'token dashboard output path: %s\n' "$TOKEN_DASHBOARD_OUTPUT_PATH"
printf 'count: %s\n' "$COUNT"
printf 'generated_at: %s\n' "$GENERATED_AT"
