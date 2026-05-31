#!/usr/bin/env python3
import subprocess
from pathlib import Path
from datetime import datetime

BASE = "main"
REPORT = Path("reports/unmerged_branches_review.md")

CODE_PATTERNS = (
    ".py", ".sh", ".js", ".jsx", ".ts", ".tsx",
    "package.json", "package-lock.json",
    ".yml", ".yaml",
)

DANGEROUS_DIRS = (
    "bots/",
    "automation/",
    "scripts/",
    "services/",
    "systemd/",
    "config/",
    ".github/",
)

DOC_DIRS = (
    "docs/",
    "projects/openclaw-knowledge-wiki/wiki/",
)


def run(cmd):
    return subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT).strip()


def safe_run(cmd):
    try:
        return run(cmd)
    except subprocess.CalledProcessError as e:
        return e.output.strip()


def classify(files, stat):
    if not stat.strip():
        return "DUPLICATE_OR_EMPTY"

    file_list = [f.strip() for f in files.splitlines() if f.strip()]

    if any(f.startswith(DANGEROUS_DIRS) for f in file_list):
        return "DANGEROUS_OR_CODE"

    if any(f.endswith(CODE_PATTERNS) for f in file_list):
        return "DANGEROUS_OR_CODE"

    if file_list and all(f.startswith(DOC_DIRS) or f.endswith(".md") for f in file_list):
        return "PR_CANDIDATE"

    if len(file_list) > 8:
        return "REVIEW_MANUALLY"

    return "REVIEW_MANUALLY"


def main():
    status = safe_run(["git", "status", "--short"])
    branches_raw = run(["git", "branch", "--no-merged", BASE, "--format=%(refname:short)"])
    branches = [b for b in branches_raw.splitlines() if b.strip()]

    lines = []
    lines.append("# Unmerged Branches Review")
    lines.append("")
    lines.append(f"- generated_at: {datetime.now().isoformat(timespec='seconds')}")
    lines.append(f"- base: `{BASE}`")
    lines.append(f"- working_tree_status: `{'clean' if not status else 'dirty'}`")
    lines.append("")
    lines.append("## Summary table")
    lines.append("")
    lines.append("| rama | clasificación | archivos | motivo | siguiente acción segura |")
    lines.append("|---|---|---:|---|---|")

    counters = {}

    details = []

    for branch in branches:
        log = safe_run(["git", "log", "--oneline", f"{BASE}..{branch}", "--max-count=5"])
        stat = safe_run(["git", "diff", "--stat", f"{BASE}...{branch}"])
        files = safe_run(["git", "diff", "--name-only", f"{BASE}...{branch}"])

        file_list = [f for f in files.splitlines() if f.strip()]
        classification = classify(files, stat)
        counters[classification] = counters.get(classification, 0) + 1

        if classification == "DUPLICATE_OR_EMPTY":
            action = "Puede limpiarse tras confirmación humana."
            motive = "Diff vacío contra main."
        elif classification == "PR_CANDIDATE":
            action = "Revisar contenido y abrir PR documental."
            motive = "Cambios documentales sin código ejecutable aparente."
        elif classification == "DANGEROUS_OR_CODE":
            action = "Revisión humana completa; no borrar ni mergear automáticamente."
            motive = "Toca código, automation, scripts, config o package-lock."
        else:
            action = "Revisar manualmente antes de decidir."
            motive = "Cambio no trivial o mixto."

        lines.append(
            f"| `{branch}` | {classification} | {len(file_list)} | {motive} | {action} |"
        )

        details.append((branch, log, stat, files))

    lines.append("")
    lines.append("## Counts")
    lines.append("")
    for key in sorted(counters):
        lines.append(f"- {key}: {counters[key]}")

    lines.append("")
    lines.append("## Details")
    lines.append("")

    for branch, log, stat, files in details:
        lines.append(f"### {branch}")
        lines.append("")
        lines.append("#### LOG")
        lines.append("```text")
        lines.append(log)
        lines.append("```")
        lines.append("")
        lines.append("#### STAT")
        lines.append("```text")
        lines.append(stat)
        lines.append("```")
        lines.append("")
        lines.append("#### FILES")
        lines.append("```text")
        lines.append(files)
        lines.append("```")
        lines.append("")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Report written: {REPORT}")


if __name__ == "__main__":
    main()

