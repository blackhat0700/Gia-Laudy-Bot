import os
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
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

# --- Fungsi Gemini ---
def ask_gemini(prompt: str):
    try:
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(GEMINI_URL, headers=headers, json=payload)
        result = response.json()
        if "candidates" in result:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return "Maaf, aku gagal merespons!"
    except Exception as e:
        return f"Error: {e}"

# --- Start Command ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Aku Gia Laudy v10 🤖 (Gemini Lite). Ayo ngobrol!")

# --- Handle Pesan ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    await update.message.chat.send_action(action="typing")
    logging.info(f"[USER] {user_msg}")

    # Custom Q&A
    if "siapa pembuatmu" in user_msg.lower():
        bot_reply = "Pembuatku adalah Hamdanu, seorang programmer yang sangat kreatif!"
    else:
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

# --- Main ---
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logging.info("Bot berjalan... Gia Laudy v10 siap!")
    app.run_polling()

if __name__ == "__main__":
    main()
