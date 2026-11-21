import os, sqlite3, time, logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
TOKEN = os.getenv("TOKEN") or os.getenv("BOT_TOKEN")
WEB_APP_URL = "https://t.me"

def init_db():
    conn = sqlite3.connect('mediamond.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (user_id INTEGER PRIMARY KEY, username TEXT, balance REAL, 
                  mining_level INTEGER, last_claim REAL, referrals INTEGER, 
                  hash_rate INTEGER, joined_at TEXT)''')
    conn.commit()
    conn.close()

def get_user(user_id):
    conn = sqlite3.connect('mediamond.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    row = c.fetchone()
    conn.close()
    return row

def create_user(user_id, username, ref_id=None):
    conn = sqlite3.connect('mediamond.db')
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users VALUES (?,?,?,?,?,?,?,?)",
              (user_id, username, 0.0, 1, time.time(), 0, 10, datetime.now().isoformat()))
    if ref_id and ref_id != user_id:
        c.execute("UPDATE users SET balance=balance+100, referrals=referrals+1 WHERE user_id=?", (ref_id,))
    conn.commit()
    conn.close()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    init_db()
    user = update.effective_user
    args = context.args
    ref_id = int(args[0]) if args and args[0].isdigit() else None
    if not get_user(user.id):
        create_user(user.id, user.username or user.first_name, ref_id)
        if ref_id:
            try: await context.bot.send_message(ref_id, f"🎉 صديق جديد سجل! ربحتي 100 MED!")
            except: pass
    u = get_user(user.id)
    kb = [
        [InlineKeyboardButton("⛏️ افتح التعدين 💎", callback_data="mine")],
        [InlineKeyboardButton(f"💰 {u[2]:.2f} MED", callback_data="balance"), InlineKeyboardButton(f"⚡ Lv {u[3]}", callback_data="level")],
        [InlineKeyboardButton("👥 رابط الإحالة", callback_data="referral"), InlineKeyboardButton("🎯 المهام", callback_data="tasks")],
    ]
    txt = f"💎 MEDIAMOND - MED COIN\n\n👤 {user.first_name}\n💰 {u[2]:.2f} MED\n⚡ Lv {u[3]} | {u[6]} MH/s\n👥 {u[5]} إحالات\n\n⛏️ كتربح {u[6]*0.01:.2f} MED/ساعة!"
    await update.message.reply_text(txt, reply_markup=InlineKeyboardMarkup(kb))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id
    u = get_user(uid)
    if not u: return
    if q.data == "mine" or q.data == "balance":
        elapsed = (time.time() - u[4]) / 3600
        mined = elapsed * u[6] * 0.01
        new_bal = u[2] + mined
        conn = sqlite3.connect('mediamond.db')
        conn.execute("UPDATE users SET balance=?, last_claim=? WHERE user_id=?", (new_bal, time.time(), uid))
        conn.commit()
        conn.close()
        await q.edit_message_text(f"✅ جمعتي {mined:.2f} MED!\n💰 الجديد: {new_bal:.2f} MED")
    elif q.data == "referral":
        bot = (await context.bot.get_me()).username
        link = f"https://t.me/{bot}?start={uid}"
        await q.edit_message_text(f"👥 رابطك:\n`{link}`\n\nكل صديق = 100 MED", parse_mode='Markdown')
    elif q.data == "tasks":
        await q.edit_message_text("🎯 المهام:\n✅ دخول يومي: +10 MED\n✅ دعوة 3 أصدقاء: ترقية\nقريبا...")
    elif q.data == "level":
        await q.edit_message_text(f"⚡ مستواك {u[3]}\nقوة {u[6]} MH/s\nدعو 3 أصدقاء باش تطلع Lv {u[3]+1}")

def main():
    if not TOKEN:
        print("❌ TOKEN missing")
        return
    init_db()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("✅ MEDIAMOND BOT READY")
    app.run_polling()

if __name__ == "__main__":
    main()
