print("Gia Laudy Level 3 sedang dijalankan...")

import logging
import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import botplus            # logika balasan + memori nama
from gtts import gTTS     # text ke suara (mp3)

# ----- LOGGING -----
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

TOKEN = "7705129606:AAE-iqQjexKjqmryO4sRnUlg6ONRK4uL78s"

# ----- COMMANDS -----
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Aku Gia Laudy Level 3. Ketik /help untuk bantuan.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Perintah Gia Laudy:\n"
        "/start - Mulai ngobrol\n"
        "/help - Tampilkan bantuan\n"
        "/about - Tentang aku\n"
        "Ketik: nama saya <nama>\n"
        "Ketik: jam berapa\n"
        "Ketik: stiker\n"
        "Ketik: suara (dapat balasan suara)"
    )

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Aku Gia Laudy v3. Dibuat di Termux, bisa simpan nama & balas suara.")

# ----- PESAN TEKS -----
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text or ""
    user_id = update.message.from_user.id

    response = botplus.get_response(user_text, user_id)

    if response == "__STIKER__":
        # stiker sample (kalau error, bot kirim teks fallback)
        try:
            await update.message.reply_sticker("CAACAgUAAxkBAAED1v5mP1qMZxP2Y7HgD8cAAf2n1u6D1gACcAgAAj-VSErYms5DiF9fNTME")
        except Exception as e:
            await update.message.reply_text(f"(Gagal kirim stiker: {e})")
        return

    if response == "__VOICE__":
        try:
            msg = "Halo! Ini suara dari Gia Laudy."
            tts = gTTS(msg, lang="id")
            fname = "gia_voice.mp3"
            tts.save(fname)
            # kirim sebagai audio (mp3); lebih aman tanpa ffmpeg
            await update.message.reply_audio(audio=open(fname, "rb"), title="Gia Laudy")
        except Exception as e:
            await update.message.reply_text(f"(Gagal bikin suara: {e})")
        finally:
            try:
                os.remove(fname)
            except:
                pass
        return

    # balasan teks biasa
    await update.message.reply_text(response)

# ----- MAIN (SINKRON, TANPA ASYNCIO.RUN) -----
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Gia Laudy: mulai polling Telegram...")
    app.run_polling()   # <-- library yang kelola event loop

if __name__ == "__main__":
    main()
