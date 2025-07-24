import os
import logging
from gtts import gTTS
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import openai
import requests

# --- Konfigurasi Logging ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# --- API Keys ---
BOT_TOKEN = "7705129606:AAHyWFFlYDqwBMdKfzpm-3RolOWfqVCFqaM"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "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")

openai.api_key = OPENAI_API_KEY

# --- Fungsi Start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Aku Gia Laudy v5 🤖. Kirim pesan untuk ngobrol denganku.")

# --- Fungsi Balas Pesan ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    await update.message.chat.send_action(action="typing")
    logging.info(f"Pesan dari user: {user_msg}")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_msg}],
            max_tokens=200
        )
        bot_reply = response["choices"][0]["message"]["content"]
        await update.message.reply_text(bot_reply)

        # Kirim suara (TTS)
        try:
            tts = gTTS(bot_reply, lang='id')
            tts.save("reply.mp3")
            await update.message.reply_audio(audio=open("reply.mp3", "rb"))
            os.remove("reply.mp3")
        except Exception as tts_err:
            logging.error(f"Error TTS: {tts_err}")
            await update.message.reply_text("Gagal mengirim audio TTS.")

    except Exception as e:
        logging.error(f"Error di OpenAI: {e}")
        await update.message.reply_text("Maaf, ada gangguan pada AI-ku!")

# --- Fungsi Kirim Stiker ---
async def send_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Pakai URL untuk unduh stiker
        sticker_url = "https://www.gstatic.com/webp/gallery/2.sm.webp"
        response = requests.get(sticker_url)
        with open("stiker.webp", "wb") as f:
            f.write(response.content)

        await update.message.reply_sticker(sticker=open("stiker.webp", "rb"))
        os.remove("stiker.webp")
    except Exception as e:
        logging.error(f"Gagal kirim stiker: {e}")
        await update.message.reply_text("__STIKER__ (Gagal kirim stiker)")

# --- Main ---
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stiker", send_sticker))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logging.info("Bot berjalan... Gia Laudy v5 siap!")
    app.run_polling()

if __name__ == "__main__":
    main()
