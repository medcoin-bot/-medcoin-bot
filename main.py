import os, requests, time
from threading import Thread

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send(text):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": text}, timeout=10)
        print(f"Sent: {text}")
    except Exception as e:
        print(f"Error: {e}")

def get_price():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=medibloc&vs_currencies=usd"
        r = requests.get(url, timeout=10).json()
        return r['medibloc']['usd']
    except:
        return None

def check_messages():
    offset = 0
    while True:
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset={offset}&timeout=15"
            res = requests.get(url, timeout=20).json()
            for upd in res.get("result", []):
                offset = upd["update_id"] + 1
                msg = upd.get("message", {}).get("text", "")
                if "/start" in msg:
                    price = get_price()
                    if price:
                        send(f"✅ البوت خدام!\nتمن MED هو: ${price}")
                    else:
                        send("✅ البوت خدام! غادي نبدا نصيفط التمن كل 5 دقايق")
        except:
            time.sleep(5)

def price_loop():
    while True:
        price = get_price()
        if price:
            send(f"💰 تمن MED: ${price}")
        time.sleep(300)

Thread(target=check_messages, daemon=True).start()
price_loop()
