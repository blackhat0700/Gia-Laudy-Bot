import random
import datetime
import json
import os

DATA_FILE = "data_user.json"

def load_user_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_user_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

user_data = load_user_data()

RESPONSES = [
    "Aku nggak yakin, tapi menarik 🤔",
    "Wah, pertanyaan bagus tuh!",
    "Menurutku tergantung kamu ❤️",
    "Hehe... aku masih belajar.",
    "Tanya lagi dong, seru nih!"
]

def get_response(message: str, user_id=None) -> str:
    text = (message or "").lower()

    # simpan nama
    if "nama saya" in text:
        name = text.replace("nama saya", "").strip().title()
        if user_id:
            user_data[str(user_id)] = name
            save_user_data(user_data)
        return f"Halo {name}! Senang kenal kamu 😊"

    # panggil nama jika dikenal
    if "nama saya siapa" in text and user_id:
        name = user_data.get(str(user_id))
        return f"Kamu belum kasih nama." if not name else f"Nama yang kamu kasih ke aku: {name}."

    if "nama kamu" in text or "siapa kamu" in text:
        return "Namaku Gia Laudy, asisten AI buatan kamu."

    if "apa kabar" in text:
        return "Aku baik, makasih! Kamu gimana?"

    if "jam berapa" in text:
        now = datetime.datetime.now().strftime("%H:%M")
        return f"Sekarang jam {now}."

    if "stiker" in text:
        return "__STIKER__"

    if "suara" in text:
        return "__VOICE__"

    return random.choice(RESPONSES)
