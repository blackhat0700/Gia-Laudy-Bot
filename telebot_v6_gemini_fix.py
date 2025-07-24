import os
import logging
from gtts import gTTS
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import google.generativeai as genai

# --- Logging ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# --- API Keys ---
BOT_TOKEN = "7705129606:AAHyWFFlYDqwBMdKfzpm-3RolOWfqVCFqaM"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBYdZtJELeDHkl7dvy1PbRMEMI_u4kzU58")

# --- Konfigurasi Gemini ---
try:
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel("gemini-1.5-flash")
    logging.info("Gemini AI siap digunakan.")
except Exception as e:
    logging.error(f"Gagal konfigurasi Gemini: {e}")
    gemini_model = None

# --- Start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Aku Gia Laudy v6 🤖 (Gemini AI). Kirim pesan untuk ngobrol denganku.")

# --- Handle Pesan ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    await update.message.chat.send_action(action="typing")

    try:
        if gemini_model:
            logging.info(f"[USER] {user_msg}")
            response = gemini_model.generate_content(user_msg)
            bot_reply = response.text.strip() if response and response.text else "(Kosong)"
        else:
            bot_reply = "Maaf, AI Gemini gagal merespons!"

        logging.info(f"[BOT] {bot_reply}")
        await update.message.reply_text(bot_reply)

        # TTS
        try:
            tts = gTTS(bot_reply, lang='id')
            tts.save("reply.mp3")
            await update.message.reply_audio(audio=open("reply.mp3", "rb"))
            os.remove("reply.mp3")
        except Exception as e:
            logging.error(f"Error TTS: {e}")

    except Exception as e:
        logging.error(f"Error Gemini: {e}")
        await update.message.reply_text("Maaf, AI Gemini gagal merespons!")

# --- Sticker ---
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

