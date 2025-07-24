import os
import logging
from gtts import gTTS
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import google.generativeai as genai
import requests
import datetime
import asyncio

# --- Logging ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# --- API Keys ---
BOT_TOKEN = "7705129606:AAHyWFFlYDqwBMdKfzpm-3RolOWfqVCFqaM"
GEMINI_API_KEY = "AIzaSyBYdZtJELeDHkl7dvy1PbRMEMI_u4kzU58"

# --- Konfigurasi Gemini ---
try:
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel("gemini-1.5-flash")
    logging.info("Gemini AI siap digunakan.")
except Exception as e:
    logging.error(f"Gagal konfigurasi Gemini: {e}")
    gemini_model = None

# --- Start Command ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Aku Gia Laudy v11 🤖 (Gemini AI). Ketik pesanmu untuk ngobrol denganku.")

# --- Command: /musik [judul] ---
async def musik(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Contoh: /musik akad payung teduh")
        return

    query = " ".join(context.args)
    await update.message.reply_text(f"Mencari musik: {query}")
    try:
        os.system(f"yt-dlp -x --audio-format mp3 -o 'musik.mp3' 'ytsearch1:{query}'")
        await update.message.reply_audio(audio=open("musik.mp3", "rb"))
        os.remove("musik.mp3")
    except Exception as e:
        await update.message.reply_text(f"Gagal ambil musik: {e}")

# --- Command: /gambar [prompt] ---
async def gambar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Contoh: /gambar pemandangan gunung indah")
        return
    prompt = " ".join(context.args)
    await update.message.reply_text(f"Fitur gambar belum support penuh di Gemini Lite.\nPrompt: {prompt}")

# --- Command: /alarm [detik] ---
async def alarm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("Contoh: /alarm 10 (untuk 10 detik)")
        return
    delay = int(context.args[0])
    await update.message.reply_text(f"Alarm diatur {delay} detik...")
    await asyncio.sleep(delay)
    await update.message.reply_text("⏰ Waktunya habis!")

# --- Handle Pesan Chat ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    await update.message.chat.send_action(action="typing")

    # Cek pertanyaan spesial
    if "pembuatmu" in user_msg.lower():
        bot_reply = "Pembuatku adalah hamdanu, seorang programmer yang sangat kreatif!"
    else:
        try:
            if gemini_model:
                response = gemini_model.generate_content(user_msg)
                bot_reply = response.text.strip() if response and response.text else "Maaf, aku gagal merespons!"
            else:
                bot_reply = "Maaf, AI Gemini gagal merespons!"
        except Exception as e:
            logging.error(f"Error Gemini: {e}")
            bot_reply = "Maaf, aku gagal merespons!"

    await update.message.reply_text(bot_reply)

    # TTS (Suara)
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
    app.add_handler(CommandHandler("musik", musik))
    app.add_handler(CommandHandler("gambar", gambar))
    app.add_handler(CommandHandler("alarm", alarm))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logging.info("Bot v11 berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
