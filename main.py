import os
import requests
import asyncio
from telegram import Bot
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "1481617690"))
CHANNEL_ID = os.getenv("CHANNEL_ID")  # غادي نزيدوه من بعد

bot = Bot(token=BOT_TOKEN)

# دالة كتجيب تمن MED
def get_med_price():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=medibloc&vs_currencies=usd"
        r = requests.get(url, timeout=10)
        price = r.json()['medibloc']['usd']
        return price
    except:
        return None

# /start
async def start(update, ContextTypes.DEFAULT_TYPE):
    price = get_med_price()
    if price:
        await update.message.reply_text(f"✅ البوت خدام!\n💰 تمن MED هو: ${price}\n\nأوامر المجتمع:\n/buy [العدد] - إلا شريتي\n/sell [العدد] - إلا بعتي\n/price - باش تشوف التمن")
    else:
        await update.message.reply_text("البوت خدام ولكن مقدرتش نجيب التمن دابا")

# /price
async def price_cmd(update, context):
    price = get_med_price()
    if price:
        await update.message.reply_text(f"💰 MED: ${price}")

# /buy - كيصيفط إشارة الشراء للمجتمع
async def buy_cmd(update, context):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ غير المهدي يقدر يصيفط إشارات!")
        return
    
    amount = " ".join(context.args) if context.args else ""
    price = get_med_price()
    
    msg_admin = f"✅ صيفطت إشارة الشراء للمجتمع!"
    await update.message.reply_text(msg_admin)
    
    # رسالة المجتمع
    community_msg = f"🚀🚀 **إشارة شراء جديدة!** 🚀🚀\n\n👑 المهدي شرا دابا!\n💰 العملة: MED\n💵 التمن: ${price}\n📦 الكمية: {amount if amount else 'ما محددش'}\n\n🔥 اللي بغا يربح يشري دابا معاه!"
    
    # صيفط للقناة إلا كاينة
    if CHANNEL_ID:
        try:
            await bot.send_message(chat_id=CHANNEL_ID, text=community_msg)
        except Exception as e:
            await update.message.reply_text(f"مقدرتش نوصط للقناة: {e}\nزيد البوت كـ Admin فالجروب!")

# /sell - إشارة البيع
async def sell_cmd(update, context):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ غير المهدي يقدر يصيفط إشارات!")
        return
        
    amount = " ".join(context.args) if context.args else ""
    price = get_med_price()
    
    await update.message.reply_text(f"✅ صيفطت إشارة البيع للمجتمع!")
    
    community_msg = f"📉📉 **إشارة بيع!** 📉📉\n\n👑 المهدي باع دابا!\n💰 العملة: MED\n💵 التمن: ${price}\n📦 الكمية: {amount if amount else 'ما محددش'}\n\n⚠️ بيعو معاه إلا بغيتو!"
    
    if CHANNEL_ID:
        try:
            await bot.send_message(chat_id=CHANNEL_ID, text=community_msg)
        except Exception as e:
            await update.message.reply_text(f"مقدرتش نوصط للقناة: {e}")

# مهمة كتصيفط التمن كل 5 دقايق
async def price_job(context: ContextTypes.DEFAULT_TYPE):
    price = get_med_price()
    if price and CHANNEL_ID:
        try:
            await bot.send_message(chat_id=CHANNEL_ID, text=f"💰 تحديث MED: ${price}")
        except:
            pass

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", price_cmd))
    app.add_handler(CommandHandler("buy", buy_cmd))
    app.add_handler(CommandHandler("sell", sell_cmd))
    
    # كل 5 دقايق صيفط التمن
    job_queue = app.job_queue
    job_queue.run_repeating(price_job, interval=300, first=10)
    
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
