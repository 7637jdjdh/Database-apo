import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from keep_alive import keep_alive

BOT_TOKEN = os.environ['BOT_TOKEN']
ALLOWED_CHAT_ID = int(os.environ['GROUP_ID'])
API_URL = os.environ['API_URL']  # JSON API from Bot Business

keep_alive()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != ALLOWED_CHAT_ID:
        return
    await update.message.reply_text("📲 Send RC or Phone number to get data.")

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != ALLOWED_CHAT_ID:
        return
    query = update.message.text.strip().replace(" ", "").replace("+91", "").lstrip("0")

    try:
        response = requests.get(API_URL)
        data = response.json()

        for item in data:
            if item.get("rc_number", "").replace(" ", "") == query or item.get("phone", "").replace(" ", "") == query:
                msg = "\n".join([f"{k}: {v}" for k, v in item.items()])
                await update.message.reply_text(f"✅ Found:\n{msg}")
                return
        await update.message.reply_text("❌ Not found.")
    except:
        await update.message.reply_text("⚠️ API Error")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))
app.run_polling()
