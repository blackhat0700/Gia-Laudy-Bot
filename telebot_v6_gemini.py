import os
import logging
from gtts import gTTS
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import requests

# --- Konfigurasi Logging ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# --- API Keys ---
BOT_TOKEN = "7705129606:AAHyWFFlYDqwBMdKfzpm-3RolOWfqVCFqaM"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBYdZtJELeDHkl7dvy1PbRMEMI_u4kzU58")

# --- Fungsi Start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Aku Gia Laudy v6 (Gemini AI) 🤖. Kirim pesan untuk ngobrol denganku.")

# --- Fungsi Balas Pesan ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    await update.message.chat.send_action(action="typing")

    try:
        # Panggil Gemini API
        response = requests.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + GEMINI_API_KEY,
            headers={"Content-Type": "application/json"},
            json={"contents": [{"parts": [{"text": user_msg}]}]}
        )

        if response.status_code == 200:
            bot_reply = response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            bot_reply = "Maaf, AI Gemini gagal merespons!"

        await update.message.reply_text(bot_reply)

        # Kirim suara (TTS)
        tts = gTTS(bot_reply, lang='id')
        tts.save("reply.mp3")
        await update.message.reply_audio(audio=open("reply.mp3", "rb"))
        os.remove("reply.mp3")

    except Exception as e:
        logging.error(f"Error di Gemini: {e}")
        await update.message.reply_text("Maaf, ada gangguan pada AI-ku!")

# --- Fungsi Kirim Stiker ---
async def send_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        sticker_url = "https://www.gstatic.com/webp/gallery/2.sm.webp"
        await update.message.reply_sticker(sticker_url)
    except Exception as e:
        logging.error(f"Gagal kirim stiker: {e}")
        await update.message.reply_text("__STIKER__ (Gagal kirim stiker)")

# --- Main ---
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stiker", send_sticker))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logging.info("Bot berjalan... Gia Laudy v6 siap!")
    app.run_polling()

if __name__ == "__main__":
    main()
