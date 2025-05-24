# ✅ telegram_bot.py (to‘liq, ALLOWED_USERS bilan boshqariladigan versiya)

import telebot
import os
import json
from config import BOT_TOKEN, ADMIN_ID

bot = telebot.TeleBot(BOT_TOKEN)
bot_state = {"paused": False}

# --- Foydalanuvchi ruxsat funksiyalari ---

def load_allowed_users():
    try:
        with open("allowed_users.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_allowed_users(users):
    with open("allowed_users.json", "w") as f:
        json.dump(users, f)

ALLOWED_USERS = load_allowed_users()

# --- Signal yuborish funksiyalari ---

def send_message(text: str):
    for user_id in ALLOWED_USERS:
        try:
            bot.send_message(user_id, text)
        except Exception as e:
            print(f"❌ {user_id} ga yuborishda xatolik: {e}")

def send_chart(image_path: str):
    for user_id in ALLOWED_USERS:
        try:
            with open(image_path, 'rb') as photo:
                bot.send_photo(user_id, photo)
        except Exception as e:
            print(f"❌ Rasm yuborishda xatolik ({user_id}): {e}")
    if os.path.exists(image_path):
        os.remove(image_path)

# --- Bot komandalar ---

@bot.message_handler(commands=['start'])
def handle_start(message):
    if message.from_user.id in ALLOWED_USERS:
        bot.send_message(message.chat.id, "✅ Botga hush kelibsiz! Siz ruxsat etilgansiz.")
    else:
        bot.reply_to(message, "❌ Sizga ruxsat yo‘q.")

@bot.message_handler(commands=['pause'])
def handle_pause(message):
    if message.from_user.id == ADMIN_ID:
        bot_state['paused'] = True
        bot.send_message(message.chat.id, "⏸ Signal yuborish to‘xtatildi.")
    else:
        bot.reply_to(message, "❌ Sizga ruxsat yo‘q.")

@bot.message_handler(commands=['resume'])
def handle_resume(message):
    if message.from_user.id == ADMIN_ID:
        bot_state['paused'] = False
        bot.send_message(message.chat.id, "▶️ Signal yuborish davom etmoqda.")
    else:
        bot.reply_to(message, "❌ Sizga ruxsat yo‘q.")

@bot.message_handler(commands=['status'])
def handle_status(message):
    if message.from_user.id == ADMIN_ID:
        state = "⏸ Pauzada" if bot_state['paused'] else "✅ Faol"
        bot.send_message(message.chat.id, f"📊 Bot holati: {state}")
    else:
        bot.reply_to(message, "❌ Sizga ruxsat yo‘q.")

# --- /adduser123456789 ---
@bot.message_handler(func=lambda m: m.text.startswith("/adduser"))
def handle_adduser(message):
    if message.from_user.id != ADMIN_ID:
        return bot.reply_to(message, "❌ Siz admin emassiz.")
    try:
        user_id = int(message.text.replace("/adduser", "").strip())
        if user_id not in ALLOWED_USERS:
            ALLOWED_USERS.append(user_id)
            save_allowed_users(ALLOWED_USERS)
            bot.reply_to(message, f"✅ {user_id} qo‘shildi.")
        else:
            bot.reply_to(message, f"⚠️ {user_id} allaqachon mavjud.")
    except ValueError:
        bot.reply_to(message, "❌ Foydalanuvchi ID xato formatda.")

# --- /killuser123456789 ---
@bot.message_handler(func=lambda m: m.text.startswith("/killuser"))
def handle_killuser(message):
    if message.from_user.id != ADMIN_ID:
        return bot.reply_to(message, "❌ Siz admin emassiz.")
    try:
        user_id = int(message.text.replace("/killuser", "").strip())
        if user_id in ALLOWED_USERS:
            ALLOWED_USERS.remove(user_id)
            save_allowed_users(ALLOWED_USERS)
            bot.reply_to(message, f"🗑 {user_id} olib tashlandi.")
        else:
            bot.reply_to(message, f"❌ {user_id} ro‘yxatda yo‘q.")
    except ValueError:
        bot.reply_to(message, "❌ Foydalanuvchi ID xato formatda.")

# --- /listusers ---
@bot.message_handler(commands=['listusers'])
def handle_listusers(message):
    if message.from_user.id != ADMIN_ID:
        return bot.reply_to(message, "❌ Siz admin emassiz.")
    if not ALLOWED_USERS:
        bot.send_message(message.chat.id, "📭 Ruxsat berilgan foydalanuvchi yo‘q.")
    else:
        user_list = "\n".join(f"{i+1}. {uid}" for i, uid in enumerate(ALLOWED_USERS))
        bot.send_message(message.chat.id, f"📋 Ruxsat berilgan foydalanuvchilar:\n\n{user_list}")

# --- Botni ishga tushurish ---
def start_bot_polling():
    print("🤖 Telegram bot ishlayapti...")
    bot.infinity_polling()

def is_paused():
    return bot_state['paused']
