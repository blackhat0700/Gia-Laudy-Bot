import os
import json
import logging
import requests
from gtts import gTTS
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# --- Logging ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# --- API Keys ---
BOT_TOKEN = "7705129606:AAHyWFFlYDqwBMdKfzpm-3RolOWfqVCFqaM"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBYdZtJELeDHkl7dvy1PbRMEMI_u4kzU58")

# --- URL Gemini ---
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

# --- Fungsi Panggil Gemini ---
def ask_gemini(prompt: str) -> str:
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    try:
        response = requests.post(GEMINI_URL, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            res_json = response.json()
            text = res_json.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
            return text.strip() if text else "Maaf, tidak ada respon dari Gemini."
        else:
            return f"Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"Error: {e}"

# --- Start Command ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Aku Gia Laudy v6 🤖 (Gemini AI HTTP). Kirim pesan untuk ngobrol denganku.")

# --- Handle Pesan ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    await update.message.chat.send_action(action="typing")

    logging.info(f"[USER] {user_msg}")
    bot_reply = ask_gemini(user_msg)
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

    logging.info("Bot berjalan... Gia Laudy v6 HTTP siap!")
    app.run_polling()

if __name__ == "__main__":
    main()
