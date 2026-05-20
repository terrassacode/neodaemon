import json
import time
import requests
from urllib.parse import quote

CONFIG = "/home/openclaw/.openclaw/openclaw.json"
API_URL = "http://127.0.0.1:5000/rag-ask"
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

    return f"{answer}\n\nConfidence: {confidence}\nScore: {score}"

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

                if text.startswith("/start"):
                    send_message(chat_id, "Neodaemon RAG activo. Envíame una pregunta.")
                    continue

                send_message(chat_id, "Consultando Neodaemon...")
                answer = ask_neodaemon(text)
                send_message(chat_id, answer)

        except Exception as e:
            print("ERROR:", e)
            time.sleep(5)

if __name__ == "__main__":
    main()
