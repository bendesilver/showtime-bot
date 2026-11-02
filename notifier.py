import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_message(text: str) -> bool:
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    r = requests.post(
        url,
        data={"chat_id": CHAT_ID, "text": text},
        timeout=15,
    )
    if not r.ok:
        print("Telegram error:", r.status_code, r.text)
    return r.ok

if __name__ == "__main__":
    send_message("✅ Test: your showtime bot is connected!")