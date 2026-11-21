import os, sqlite3, logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
TOKEN = os.getenv("BOT_TOKEN") or os.getenv("TOKEN") or os.getenv("BOT_TOKEN_MINE")

def init_db():
    conn = sqlite3.connect('mediamond.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (user_id INTEGER PRIMARY KEY, mining_level INTEGER, hash_rate INTEGER, joined TEXT)''')
    conn.commit()
    conn.close()

def get_user(user_id):
    conn = sqlite3.connect('mediamond.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    row = c.fetchone()
    conn.close()
    return row

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    init_db()
    conn = sqlite3.connect('mediamond.db')
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (user_id, mining_level, hash_rate, joined) VALUES (?, 1, 10, datetime('now'))", (user_id,))
    conn.commit()
    conn.close()
    
    keyboard = [
        [InlineKeyboardButton("⛏️ بدا التعدين", callback_data="mine")],
        [InlineKeyboardButton("💰 الرصيد", callback_data="balance")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f"✅ مرحبا {update.effective_user.first_name}!\n🚀 MedCoin Bot خدام دابا!\n\n⛏️ التعدين شغال", reply_markup=reply_markup)

def main():
    if not TOKEN:
        print("❌ TOKEN ما كاينش! زيد BOT_TOKEN فـ Railway Variables")
        return
    init_db()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("🚀 Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
