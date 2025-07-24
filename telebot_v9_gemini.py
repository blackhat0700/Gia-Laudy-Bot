import os
import logging
import asyncio
from gtts import gTTS
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import google.generativeai as genai
import yt_dlp

# --- Logging ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# --- API KEYS ---
BOT_TOKEN = "7705129606:AAHyWFFlYDqwBMdKfzpm-3RolOWfqVCFqaM"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBYdZtJELeDHkl7dvy1PbRMEMI_u4kzU58")

# --- Gemini Config ---
try:
    genai.configure(api_key=GEMINI_API_KEY)
    gemini = genai.GenerativeModel("gemini-1.5-flash")
    logging.info("Gemini AI siap digunakan.")
except Exception as e:
    logging.error(f"Gagal inisialisasi Gemini: {e}")
    gemini = None

# --- Start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Aku Gia Laudy v9 (Gemini). Kirim pesanmu!")

# --- Chat Handler ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    await update.message.chat.send_action(action="typing")
    try:
        if gemini:
            response = gemini.generate_content(user_msg)
            bot_reply = response.text.strip() if response and response.text else "(Kosong)"
        else:
            bot_reply = "Maaf, AI Gemini gagal merespons!"
        await update.message.reply_text(bot_reply)

        # TTS
        try:
            tts = gTTS(bot_reply, lang="id")
            tts.save("reply.mp3")
            await update.message.reply_audio(audio=open("reply.mp3", "rb"))
            os.remove("reply.mp3")
        except Exception as e:
            logging.error(f"TTS error: {e}")

    except Exception as e:
        logging.error(f"Gemini error: {e}")
        await update.message.reply_text("Maaf, AI Gemini gagal merespons!")

# --- Musik ---
async def musik(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Gunakan format: /musik <judul lagu>")
        return
    query = " ".join(context.args)
    await update.message.reply_text(f"🔍 Mencari lagu: {query}")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "musik.%(ext)s",
        "quiet": True,
        "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}]
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{query}", download=True)
            file_name = ydl.prepare_filename(info["entries"][0]).replace(".webm", ".mp3")
        await update.message.reply_audio(audio=open(file_name, "rb"), title=query)
        os.remove(file_name)
    except Exception as e:
        logging.error(f"Musik error: {e}")
        await update.message.reply_text("Gagal mengambil musik!")

# --- Alarm ---
async def alarm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Format: /alarm <detik> <pesan>")
        return
    try:
        delay = int(context.args[0])
        pesan = " ".join(context.args[1:])
        await update.message.reply_text(f"⏳ Alarm diset {delay} detik untuk pesan: {pesan}")
        await asyncio.sleep(delay)
        await update.message.reply_text(f"⏰ Alarm: {pesan}")
    except ValueError:
        await update.message.reply_text("Gunakan angka detik yang valid!")

# --- Stiker ---
async def stiker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_sticker("https://www.gstatic.com/webp/gallery/2.sm.webp")

# --- Main ---
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("musik", musik))
    app.add_handler(CommandHandler("alarm", alarm))
    app.add_handler(CommandHandler("stiker", stiker))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logging.info("Gia Laudy v9 Gemini berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
