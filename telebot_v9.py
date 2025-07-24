import os
import logging
from gtts import gTTS
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI

# --- Logging ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# --- API Keys ---
BOT_TOKEN = "7705129606:AAHyWFFlYDqwBMdKfzpm-3RolOWfqVCFqaM"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "AIzaSyBYdZtJELeDHkl7dvy1PbRMEMI_u4kzU58")

client = OpenAI(api_key=OPENAI_API_KEY)

# --- Start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Aku Gia Laudy v9 🤖 Siap ngobrol, gambar, dan kirim lagu!")

# --- Chat ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text

    # Jawaban khusus
    if "siapa pembuatmu" in user_msg.lower():
        await update.message.reply_text("Pembuatku adalah Hamdanu, seorang programmer yang sangat kreatif!")
        return

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": user_msg}]
        )
        bot_reply = response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Error OpenAI: {e}")
        bot_reply = "Maaf, aku gagal merespons!"

    await update.message.reply_text(bot_reply)

    # TTS
    try:
        tts = gTTS(bot_reply, lang='id')
        tts.save("reply.mp3")
        await update.message.reply_audio(audio=open("reply.mp3", "rb"))
        os.remove("reply.mp3")
    except Exception as e:
        logging.error(f"Error TTS: {e}")

# --- Gambar AI ---
async def gambar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args)
    if not prompt:
        await update.message.reply_text("Contoh: /gambar kucing lucu di luar angkasa")
        return

    try:
        result = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="512x512"
        )
        image_url = result.data[0].url
        await update.message.reply_photo(image_url, caption=f"Gambar untuk: {prompt}")
    except Exception as e:
        logging.error(f"Error Gambar: {e}")
        await update.message.reply_text("Gagal membuat gambar!")

# --- Download Lagu ---
async def lagu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("Contoh: /lagu bunga citra lestari")
        return

    await update.message.reply_text(f"Mencari lagu: {query} ...")

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'outtmpl': 'lagu.mp3',
            'quiet': True,
            'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=True)
        await update.message.reply_audio(audio=open("lagu.mp3", "rb"), title=query)
        os.remove("lagu.mp3")
    except Exception as e:
        logging.error(f"Error Lagu: {e}")
        await update.message.reply_text("Gagal mengunduh lagu!")

# --- Main ---
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("gambar", gambar))
    app.add_handler(CommandHandler("lagu", lagu))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logging.info("Bot v9 berjalan... Gia Laudy siap!")
    app.run_polling()

if __name__ == "__main__":
    main()
