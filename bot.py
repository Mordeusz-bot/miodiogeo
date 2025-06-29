import os
import logging
import openai
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_NAME = "Diogenes"

# Tokeny
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Logi
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Jestem {BOT_NAME}. Pytaj, ale licz się z odpowiedzią.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://t.me/Diogenessa_bot",
        "X-Title": "DiogenesBot"
    }
    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "system", "content": "Jesteś Diogenesem z Synopy. Odpowiadaj krótko, zgryźliwie, bezczelnie."},
                     {"role": "user", "content": prompt}],
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", json=data, headers=headers)
    if response.status_code == 200:
        message = response.json()["choices"][0]["message"]["content"]
        await update.message.reply_text(message)
    else:
        await update.message.reply_text("Nie mogę teraz odpowiedzieć. Może zajrzyj do beczki...")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
