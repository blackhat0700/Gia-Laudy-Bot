import os
import logging
import asyncio
from gtts import gTTS
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import datetime
import requests

# --- Logging ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BOT_TOKEN = "7705129606:AAHyWFFlYDqwBMdKfzpm-3RolOWfqVCFqaM"

# --- Start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Halo! Aku Gia Laudy v7 🤖.\n"
        "Fitur: ngobrol, gambar (/gambar), musik (/musik), alarm (/alarm).\n"
        "Ketik pesanmu sekarang!"
    )

# --- Gambar AI (Dummy pakai URL random) ---
async def gambar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query = " ".join(context.args) if context.args else "pemandangan indah"
        img_url = f"https://source.unsplash.com/600x400/?{query}"
        await update.message.reply_photo(photo=img_url, caption=f"Hasil gambar: {query}")
    except Exception as e:
        logging.error(f"Error gambar: {e}")
        await update.message.reply_text("Gagal buat gambar.")

# --- Musik / Lagu ---
async def musik(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Contoh lagu bebas (free music)
        url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
        r = requests.get(url, stream=True)
        filename = "lagu.mp3"
        with open(filename, "wb") as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
        await update.message.reply_audio(audio=InputFile(filename), caption="Ini musiknya 🎵")
        os.remove(filename)
    except Exception as e:
        logging.error(f"Error musik: {e}")
        await update.message.reply_text("Gagal kirim musik.")

# --- Alarm ---
alarms = {}

async def alarm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if len(context.args) < 1:
            await update.message.reply_text("Format: /alarm <detik>")
            return
        seconds = int(context.args[0])
        chat_id = update.message.chat_id

        async def send_alarm():
            await asyncio.sleep(seconds)
            await context.bot.send_message(chat_id, f"⏰ Alarm selesai {seconds} detik!")
        asyncio.create_task(send_alarm())

        await update.message.reply_text(f"Alarm diatur {seconds} detik.")
    except Exception as e:
        logging.error(f"Error alarm: {e}")
        await update.message.reply_text("Gagal set alarm.")

# --- Chat AI Dummy ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text.lower()
    if "siapa pembuatmu" in user_msg:
        bot_reply = "Pembuatku adalah Hamdanu, seorang programmer yang sangat kreatif!"
    else:
        bot_reply = f"Kamu bilang: {user_msg}. Aku masih versi dummy ya 😅"
    await update.message.reply_text(bot_reply)

    # Kirim TTS
    try:
        tts = gTTS(bot_reply, lang='id')
        tts.save("reply.mp3")
        await update.message.reply_audio(audio=open("reply.mp3", "rb"))
        os.remove("reply.mp3")
    except Exception as e:
        logging.error(f"TTS Error: {e}")

# --- Main ---
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("gambar", gambar))
    app.add_handler(CommandHandler("musik", musik))
    app.add_handler(CommandHandler("alarm", alarm))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logging.info("Bot Gia Laudy v7 berjalan!")
    app.run_polling()

if __name__ == "__main__":
    main()
