import json
import time
import requests
from urllib.parse import quote
from main_handler import ask_main

CONFIG = "/home/openclaw/.openclaw/openclaw.json"
API_URL = "http://127.0.0.1:5001/rag-ask"
API_TOKEN = "neodaemon-secure-token"

with open(CONFIG) as f:
    cfg = json.load(f)

tg = cfg["channels"]["telegram"]
BOT_TOKEN = tg["botToken"]
ALLOW_FROM = set(str(x) for x in tg.get("allowFrom", []))

BASE = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_message(chat_id, text):
    max_len = 3900
    for i in range(0, len(text), max_len):
        requests.post(
            f"{BASE}/sendMessage",
            json={"chat_id": chat_id, "text": text[i:i+max_len]},
            timeout=20
        )

def ask_neodaemon(question):
    r = requests.get(
        API_URL,
        params={"token": API_TOKEN, "q": question},
        timeout=180
    )
    r.raise_for_status()
    data = r.json()

    answer = data.get("answer", "Sin respuesta")
    confidence = data.get("confidence", "n/a")
    score = data.get("score_max", "n/a")

    try:
        score_val = float(score)
        score_str = f"{score_val:.2f}"
    except:
        score_str = str(score)

    return f"{answer}\n\nConfidence: {confidence}\nScore: {score_str}"

def main():
    offset = None
    print("Telegram RAG bot running")

    while True:
        try:
            params = {"timeout": 30}
            if offset is not None:
                params["offset"] = offset

            updates = requests.get(f"{BASE}/getUpdates", params=params, timeout=40).json()

            for u in updates.get("result", []):
                offset = u["update_id"] + 1

                msg = u.get("message") or {}
                text = msg.get("text", "").strip()
                chat = msg.get("chat", {})
                user = msg.get("from", {})
                chat_id = chat.get("id")
                user_id = str(user.get("id"))

                if not text or not chat_id:
                    continue

                if ALLOW_FROM and user_id not in ALLOW_FROM:
                    send_message(chat_id, "No autorizado.")
                    continue

                if text.lower().startswith("/main"):
                    question = text[5:].strip()
                    if not question:
                        send_message(chat_id, "Uso: /main tu mensaje")
                        continue
                    answer = ask_main(question)
                    send_message(chat_id, answer)
                    continue

                if text.startswith("/start"):
                    send_message(chat_id, "Neodaemon RAG activo. Usa: /rag tu pregunta")
                    continue

                
                if text.lower().startswith("/top"):
                    import json
                    from pathlib import Path

                    C = Path("/openclaw/workspace/main/rag_store/candidates")
                    items = []

                    for f in C.glob("*.json"):
                        d = json.loads(f.read_text())
                        items.append((d.get("rank_score", 0), d))

                    items = sorted(items, key=lambda x: x[0], reverse=True)[:5]

                    msg = "Top contenidos:\n\n"
                    for i,(score,d) in enumerate(items,1):
                        title = d.get("title","")
                        url = d.get("url","")
                        typ = d.get("type","web")

                        msg += f"{i}. {title}\n"
                        msg += f"   Score: {score} | Type: {typ}\n"
                        msg += f"   {url}\n\n"
                        

                    send_message(chat_id, msg)
                    continue

                
                if text.lower().startswith("/approve"):
                    import json, shutil, subprocess
                    from pathlib import Path

                    try:
                        n = int(text.split()[1])
                    except:
                        send_message(chat_id, "Uso: /approve N")
                        continue

                    C = Path("/openclaw/workspace/main/rag_store/candidates")
                    A = Path("/openclaw/workspace/main/rag_store/approved")

                    items = []
                    for f in C.glob("*.json"):
                        d = json.loads(f.read_text())
                        items.append((d.get("rank_score",0), f, d.get("title","")))

                    items = sorted(items, reverse=True)

                    if n < 1 or n > len(items):
                        send_message(chat_id, "Número fuera de rango")
                        continue

                    _, fpath, title = items[n-1]

                    shutil.move(str(fpath), str(A / fpath.name))

                    # procesar automáticamente
                    subprocess.run([
                        "/openclaw/venvs/api/bin/python",
                        "/openclaw/bots/process_approved.py"
                    ])

                    send_message(chat_id, f"Aprobado: {title}")
                    continue

                
                if text.lower().startswith("/resumen"):
                    import json
                    from pathlib import Path

                    C = Path("/openclaw/workspace/main/rag_store/candidates")
                    items = []

                    for f in C.glob("*.json"):
                        d = json.loads(f.read_text())
                        items.append((d.get("rank_score", 0), d))

                    items = sorted(items, key=lambda x: x[0], reverse=True)[:5]

                    if not items:
                        send_message(chat_id, "No hay candidatos pendientes.")
                        continue

                    msg = "Resumen del día:\n\n"

                    for i, (score, d) in enumerate(items, 1):
                        title = d.get("title", "")

                        resumen = ""
                        t = title.lower()

                        if "dax" in t:
                            resumen = "Nueva capacidad relacionada con DAX o consultas."
                        elif "semantic model" in t:
                            resumen = "Cambios en modelos semánticos."
                        elif "fabric" in t:
                            resumen = "Novedades en Microsoft Fabric."
                        elif "api" in t:
                            resumen = "Nueva funcionalidad vía API."
                        else:
                            resumen = "Actualización relevante en plataforma de datos."

                        msg += f"{i}. {title}\n→ {resumen}\n\n"

                    msg += "Recomendación: revisa los 2 primeros."

                    send_message(chat_id, msg)
                    continue



                if not text.lower().startswith("/rag"):
                    continue

                question = text[4:].strip()
                if not question:
                    send_message(chat_id, "Uso: /rag tu pregunta")
                    continue

                answer = ask_neodaemon(question)
                send_message(chat_id, answer)
                continue

        except Exception as e:
            print("ERROR:", e)
            time.sleep(5)

if __name__ == "__main__":
    main()
