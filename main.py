
import os, requests, time
from datetime import datetime

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send(msg):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
        print(f"Sent: {msg}")
    except Exception as e:
        print(f"Error: {e}")

def get_med_price():
    try:
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=medibloc&vs_currencies=usd", timeout=10).json()
        return r['medibloc']['usd']
    except:
        return None

if not BOT_TOKEN or not CHAT_ID:
    print("Missing BOT_TOKEN or CHAT_ID")
    exit()

send(f"✅ MED COIN BOT بدا خدام! {datetime.now().strftime('%H:%M')}")
print("Bot started - Tracking MED")

while True:
    price = get_med_price()
    if price:
        msg = f"💰 MED = ${price}\n⏰ {datetime.now().strftime('%H:%M:%S')}"
        send(msg)
    time.sleep(300)
