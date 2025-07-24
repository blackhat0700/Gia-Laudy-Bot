import os
import logging
from gtts import gTTS
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI
import datetime

# --- Logging ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# --- API Keys ---
BOT_TOKEN = "7705129606:AAHyWFFlYDqwBMdKfzpm-3RolOWfqVCFqaM"  # ganti dengan token bot Telegram-mu
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "AIzaSyBYdZtJELeDHkl7dvy1PbRMEMI_u4kzU58")

# --- OpenAI Client ---
client = OpenAI(api_key=OPENAI_API_KEY)

# --- Start Command ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Aku Gia Laudy v8 🤖. Siap ngobrol denganmu!")

# --- Fitur Alarm ---
async def alarm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏰ Alarm sederhana belum diaktifkan. (Fitur demo)")

# --- Fitur Pesan ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text.strip()
    await update.message.chat.send_action(action="typing")

    # Cek pertanyaan "siapa pembuatmu"
    if "pembuatmu" in user_msg.lower():
        bot_reply = "Pembuatku adalah Hamdanu, seorang programmer yang sangat kreatif! 😎"
    elif "jam berapa" in user_msg.lower():
        bot_reply = f"Sekarang pukul {datetime.datetime.now().strftime('%H:%M:%S')}."
    else:
        try:
            logging.info(f"[USER] {user_msg}")
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": user_msg}]
            )
            bot_reply = response.choices[0].message.content.strip()
        except Exception as e:
            logging.error(f"Error OpenAI: {e}")
            bot_reply = "Maaf, aku gagal merespons!"

    logging.info(f"[BOT] {bot_reply}")
    await update.message.reply_text(bot_reply)

    # Kirim suara TTS
    try:
        tts = gTTS(bot_reply, lang='id')
        tts.save("reply.mp3")
        await update.message.reply_audio(audio=open("reply.mp3", "rb"))
        os.remove("reply.mp3")
    except Exception as e:
        logging.error(f"Error TTS: {e}")

# --- Main ---
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("alarm", alarm))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logging.info("Bot berjalan... Gia Laudy v8 siap!")
    app.run_polling()

if __name__ == "__main__":
    main()
