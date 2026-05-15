import subprocess
import json
from pathlib import Path

IDENTITY = Path("/openclaw/bots/neodaemon_identity.txt").read_text()

def find_key(obj, key):
    if isinstance(obj, dict):
        if key in obj:
            return obj[key]
        for v in obj.values():
            found = find_key(v, key)
            if found:
                return found
    elif isinstance(obj, list):
        for item in obj:
            found = find_key(item, key)
            if found:
                return found
    return None

def ask_main(question):
    message = f"""{IDENTITY}

Mensaje de Albert:
{question}
"""

    result = subprocess.run(
        [
            "openclaw", "agent",
            "--agent", "main",
            "--session-id", "telegram-main",
            "--message", message,
            "--json",
            "--thinking", "medium",
            "--timeout", "600"
        ],
        capture_output=True,
        text=True,
        timeout=650
    )

    if result.returncode != 0:
        return f"Error Neodaemon:\n{result.stderr.strip()}"

    try:
        data = json.loads(result.stdout)
        return find_key(data, "finalAssistantVisibleText") or "Sin respuesta"
    except Exception as e:
        return f"Error parseando respuesta:\n{e}"
