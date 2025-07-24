import os
import logging
import requests
from gtts import gTTS
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# --- KONFIGURASI ---
BOT_TOKEN = "7705129606:AAHyWFFlYDqwBMdKfzpm-3RolOWfqVCFqaM"
GEMINI_API_KEY = "AIzaSyBYdZtJELeDHkl7dvy1PbRMEMI_u4kzU58"  # contoh: AIzaSy... (Google AI Studio)

# --- Logging ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# --- START ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Aku Gia Laudy v9 🤖 (Gemini Lite). Ayo ngobrol!")

# --- FUNGSI PANGGIL GEMINI ---
def gemini_reply(prompt: str) -> str:
    try:
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        headers = {"Content-Type": "application/json"}
        data = {"contents": [{"parts": [{"text": prompt}]}]}
        response = requests.post(url, headers=headers, json=data, timeout=15)
        if response.status_code == 200:
            result = response.json()
            return result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "Maaf, aku gagal merespons!")
        else:
            return f"Error {response.status_code}: {response.text}"
    except Exception as e:
        logging.error(f"Gemini error: {e}")
        return "Maaf, AI gagal merespons!"

# --- HANDLE PESAN ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    await update.message.chat.send_action("typing")

    # Jawaban custom
    if "siapa pembuatmu" in user_msg.lower():
        bot_reply = "Pembuatku adalah Hamdanu, seorang programmer yang sangat kreatif."
    else:
        bot_reply = gemini_reply(user_msg)

    await update.message.reply_text(bot_reply)

    # Kirim TTS
    try:
        tts = gTTS(bot_reply, lang='id')
        tts.save("tts_reply.mp3")
        await update.message.reply_audio(audio=open("tts_reply.mp3", "rb"))
        os.remove("tts_reply.mp3")
    except Exception as e:
        logging.error(f"Error TTS: {e}")

# --- MAIN ---
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logging.info("Bot v9 Gemini Lite siap berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
