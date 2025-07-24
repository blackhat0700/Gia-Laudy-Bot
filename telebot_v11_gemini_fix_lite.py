import logging
import datetime
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai

# ==================== KONFIGURASI ====================
BOT_TOKEN = "7705129606:AAHyWFFlYDqwBMdKfzpm-3RolOWfqVCFqaM"
GEMINI_API_KEY = "AIzaSyBYdZtJELeDHkl7dvy1PbRMEMI_u4kzU58"

genai.configure(api_key=GEMINI_API_KEY)

# ==================== LOGGING ====================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==================== FUNGSI CEK WAKTU ====================
def cek_waktu():
    now = datetime.datetime.now()
    jam = now.hour
    if 5 <= jam < 12:
        return "Sekarang pagi."
    elif 12 <= jam < 18:
        return "Sekarang siang."
    elif 18 <= jam < 22:
        return "Sekarang malam."
    else:
        return "Sekarang tengah malam."

# ==================== HANDLER ====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Aku Gia Laudy v11, powered by Gemini 😊")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    user_name = update.message.from_user.first_name

    # Fitur khusus
    if "siapa pembuatmu" in text:
        await update.message.reply_text("Pembuatku adalah Hamdanu, seorang programmer yang sangat kreatif! 🤖")
        return

    if "malam atau pagi" in text:
        await update.message.reply_text(cek_waktu())
        return

    if "jam berapa" in text:
        jam_sekarang = datetime.datetime.now().strftime("%H:%M:%S")
        await update.message.reply_text(f"Sekarang jam {jam_sekarang}")
        return

    # Jawaban AI dari Gemini
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(f"{user_name} berkata: {update.message.text}")
        await update.message.reply_text(response.text)
    except Exception as e:
        logger.error(f"Error dari Gemini: {e}")
        await update.message.reply_text("Maaf, aku gagal merespons!")

# ==================== MAIN ====================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("Bot v11 Gemini Lite berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
