import os, requests, time
from datetime import datetime

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send(msg):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
    except: pass

if BOT_TOKEN and CHAT_ID:
    send(f"MED COIN BOT خدام! الوقت: {datetime.now()}")
    
print("Bot started")
while True:
    time.sleep(60)
