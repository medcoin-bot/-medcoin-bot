import os, logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
logging.basicConfig(level=logging.INFO)
TOKEN = os.getenv("9138560308:AAHZ4_SUg6c2xgN824VzfJ5hTB804w4dROU")
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ مرحبا! 🚀 MedCoin Bot خدام دابا!")
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
if __name__ == "__main__":
    main()
