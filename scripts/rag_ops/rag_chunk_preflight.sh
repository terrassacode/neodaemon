#!/usr/bin/env bash
set -euo pipefail

SCRIPT="rag_chunk_preflight.sh"
MODE="readonly_chunk_preflight"
PILOT=false
FILE=""

usage() {
  echo "USAGE=$SCRIPT [--pilot] <chunk.json>"
}

if [ "$#" -eq 0 ]; then
  usage
  exit 2
fi

if [ "${1:-}" = "--pilot" ]; then
  PILOT=true
  shift
fi

FILE="${1:-}"

if [ -z "$FILE" ]; then
  usage
  exit 2
fi

echo "STATUS=START"
echo "SCRIPT=$SCRIPT"
echo "MODE=$MODE"
echo "PILOT=$PILOT"
echo "FILE=$FILE"

if [ ! -f "$FILE" ]; then
  echo "STATUS=ERROR"
  echo "RESULT=preflight_failed"
  echo "ERROR=file_not_found"
  exit 1
fi

python3 - "$FILE" "$PILOT" <<'PY'
import json
import re
import sys
from pathlib import Path

path = Path(sys.argv[1])
pilot = sys.argv[2].lower() == "true"

errors = []
warnings = []

def check(name, ok, message=""):
    print(f"CHECK_{name}={'ok' if ok else 'fail'}" + (f" MESSAGE={message}" if message else ""))
    if not ok:
        errors.append(name)

try:
    raw = path.read_text(encoding="utf-8")
    data = json.loads(raw)
    print("CHECK_json=ok")
except Exception as exc:
    print("CHECK_json=fail MESSAGE=" + str(exc).replace("\n", " "))
    print("STATUS=ERROR")
    print("RESULT=preflight_failed")
    sys.exit(1)

text = data.get("text")
content = data.get("content")
status = data.get("status")
validation = data.get("validation")
quality_score = data.get("quality_score")
combined = "\n".join(str(v) for v in data.values() if isinstance(v, (str, int, float)))
combined_lower = combined.lower()

check("text_present", isinstance(text, str) and len(text.strip()) > 0)
check("content_present", isinstance(content, str) and len(content.strip()) > 0)
check("text_equals_content", isinstance(text, str) and isinstance(content, str) and text == content)

allowed_status = {"draft", "review", "approved", "quarantine", "deprecated"}
check("status_allowed", status in allowed_status, f"status={status!r}")
check("status_not_conditioned", status != "conditioned")

expected_status = {
    "A": "approved",
    "B": "review",
    "C": "quarantine",
    "D": "deprecated",
}
if validation in expected_status:
    check("validation_status_compatible", status == expected_status[validation], f"validation={validation!r} status={status!r}")
else:
    check("validation_status_compatible", False, f"validation={validation!r}")

check("known_typo_siexiste", "siexiste" not in combined_lower)

has_15 = bool(re.search(r"(?<!\d)1[\.,]5(?!\d)", combined))
has_provisional = "provisional" in combined_lower
check("threshold_15_provisional", (not has_15) or has_provisional)

has_nugget = "nugget" in combined_lower
has_no_predice = "no predice" in combined_lower or "no predec" in combined_lower
has_no_garantiza = "no garantiza" in combined_lower or "no garant" in combined_lower
check("nugget_guardrail", (not has_nugget) or has_no_predice or has_no_garantiza)

if pilot:
    check("pilot_quality_score_zero", quality_score == 0, f"quality_score={quality_score!r}")
    check("pilot_validation_B", validation == "B", f"validation={validation!r}")
    check("pilot_status_review", status == "review", f"status={status!r}")
else:
    if quality_score != 0:
        warnings.append("quality_score_not_zero_non_pilot")

for warning in warnings:
    print(f"WARNING={warning}")

if errors:
    print("STATUS=ERROR")
    print("RESULT=preflight_failed")
    print("FAILED_CHECKS=" + ",".join(errors))
    sys.exit(1)

print("STATUS=OK")
print("RESULT=preflight_passed")
print("NEXT=Run JSON validation and BM25 only if this preflight is for an operational pilot chunk.")
PY
