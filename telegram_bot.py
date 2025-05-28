# ✅ telegram_bot.py – Mukammal Telegram AI Bot moduli
import telebot
import os
import json
import time
import threading
import pandas as pd
from ai_model import train_ai_model, predict_from_model
from logger import clean_signals
from config import BOT_TOKEN, ADMIN_ID, BACKTEST_MATRIX, BACKTEST_CONFIDENCE


bot = telebot.TeleBot(BOT_TOKEN)
bot_state = {"paused": False}

# --- Ruxsat etilgan foydalanuvchilarni boshqarish
ALLOWED_FILE = "allowed_users.json"

def load_allowed_users():
    try:
        with open(ALLOWED_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_allowed_users(users):
    with open(ALLOWED_FILE, "w") as f:
        json.dump(users, f)

ALLOWED_USERS = load_allowed_users()

# --- Yuborish funksiyalari
def send_message(text):
    for user_id in ALLOWED_USERS:
        try:
            bot.send_message(user_id, text)
        except Exception as e:
            print(f"❌ {user_id} ga yuborilmadi: {e}")

def send_chart(path, caption=None):
    for user_id in ALLOWED_USERS:
        try:
            with open(path, 'rb') as photo:
                bot.send_photo(user_id, photo, caption=caption)
        except Exception as e:
            print(f"❌ {user_id} rasm yuborilmadi: {e}")
    if os.path.exists(path):
        os.remove(path)

# --- Telegram komandalar
@bot.message_handler(commands=['start'])
def handle_start(message):
    if message.from_user.id in ALLOWED_USERS:
        bot.send_message(message.chat.id, "✅ Hush kelibsiz! Sizga ruxsat bor.")
    else:
        bot.reply_to(message, "❌ Sizga ruxsat yo‘q.")

@bot.message_handler(commands=['pause'])
def handle_pause(message):
    if message.from_user.id == ADMIN_ID:
        bot_state['paused'] = True
        bot.send_message(message.chat.id, "⏸ Pauza bosildi.")
    else:
        bot.reply_to(message, "❌ Siz admin emassiz.")

@bot.message_handler(commands=['resume'])
def handle_resume(message):
    if message.from_user.id == ADMIN_ID:
        bot_state['paused'] = False
        bot.send_message(message.chat.id, "▶️ Faollik tiklandi.")
    else:
        bot.reply_to(message, "❌ Siz admin emassiz.")

@bot.message_handler(commands=['status'])
def handle_status(message):
    if message.from_user.id == ADMIN_ID:
        state = "⏸ Pauzada" if bot_state['paused'] else "✅ Faol"
        bot.send_message(message.chat.id, f"📊 Bot holati: {state}")
    else:
        bot.reply_to(message, "❌ Siz admin emassiz.")

@bot.message_handler(commands=['help'])
def handle_help(message):
    help_text = (
        "📘 Komandalar:"

        "/start – Botga kirish "
        "/pause – Botni to‘xtatish (ADMIN) "
        "/resume – Botni yoqish (ADMIN) "
        "/status – Bot holatini ko‘rish "
        "/filter [15min] – Timeframe bo‘yicha signal "
        "/filterfoiz [80] – Confidence bo‘yicha "
        "/statistika – Signal statistikasi "
        "/reset – Modelni qayta o‘qitish "
        "/tozalash – Tozalash (clean_signals.csv) "
        "/info – Model oxirgi signal tahlili "
        "/baborat [8ta raqam] – AI bashorat "
        "/csv – CSV faylni yuborish "
        "/grafik – AI confusion matrix grafigi "
        
)
    bot.send_message(message.chat.id, help_text)

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

@bot.message_handler(commands=['users'])
def handle_users(message):
    if message.from_user.id != ADMIN_ID:
        return bot.reply_to(message, "❌ Siz admin emassiz.")
    text = "👥 Ruxsat etilganlar:\n" + "\n".join([str(u) for u in ALLOWED_USERS])
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['csv'])
def handle_csv(message):
    if message.from_user.id != ADMIN_ID:
        return bot.reply_to(message, "❌ Siz admin emassiz.")
    try:
        with open("signals.csv", 'rb') as file:
            bot.send_document(message.chat.id, file)
    except:
        bot.send_message(message.chat.id, "❌ Fayl mavjud emas.")

@bot.message_handler(commands=['filter'])
def handle_filter(message):
    try:
        args = message.text.split()
        if len(args) < 2:
            return bot.reply_to(message, "❌ Foydalanish: /filter 15min")
        tf = args[1]
        df = pd.read_csv("signals.csv")
        filtered = df[df['timeframe'] == tf]
        if filtered.empty:
            bot.reply_to(message, f"⛔ {tf} uchun signal topilmadi.")
        else:
            rows = filtered.tail(5).to_string(index=False)
            bot.reply_to(message, f"🗂 Oxirgi 5 ta signal:\n<pre>{rows}</pre>", parse_mode="HTML")
    except Exception as e:
        bot.reply_to(message, f"❌ Xatolik: {e}")

@bot.message_handler(commands=['filterfoiz'])
def handle_filterfoiz(message):
    try:
        args = message.text.split()
        if len(args) < 2:
            return bot.reply_to(message, "❌ Foydalanish: /filterfoiz 80")
        thres = float(args[1])
        df = pd.read_csv("signals.csv")
        filtered = df[df['confidence'] >= thres / 100.0]
        if filtered.empty:
            bot.reply_to(message, f"⛔ {thres}%+ signal topilmadi.")
        else:
            rows = filtered.tail(5).to_string(index=False)
            bot.reply_to(message, f"🔍 Oxirgi 5 ta signal:\n<pre>{rows}</pre>", parse_mode="HTML")
    except Exception as e:
        bot.reply_to(message, f"❌ Xatolik: {e}")

@bot.message_handler(commands=['statistika'])
def handle_statistika(message):
    try:
        df = pd.read_csv("signals.csv")
        buy = df[df['signal'].str.lower().str.contains('buy')].shape[0]
        sell = df[df['signal'].str.lower().str.contains('sell')].shape[0]
        kuchli = df[df['signal'].str.contains("KUCHLI", case=False)].shape[0]
        tf_stats = df['timeframe'].value_counts().to_dict()
        tf_lines = " | ".join([f"{k}({v})" for k, v in tf_stats.items()])
        bot.send_message(message.chat.id, f"📊 Statistika:\nBuy: {buy} | Sell: {sell} | KUCHLI: {kuchli}\nTF: {tf_lines}")
    except Exception as e:
        bot.reply_to(message, f"❌ Xatolik: {e}")

@bot.message_handler(commands=['reset'])
def handle_reset(message):
    if message.from_user.id != ADMIN_ID:
        return bot.reply_to(message, "❌ Siz admin emassiz.")
    def train_thread():
        try:
            bot.send_message(message.chat.id, "🔄 Model qayta o‘qitilmoqda...")
            train_ai_model()
            bot.send_message(message.chat.id, "✅ Model yangilandi!")
        except Exception as e:
            bot.send_message(message.chat.id, f"❌ Model o‘qitishda xatolik: {e}")
    threading.Thread(target=train_thread, daemon=True).start()

@bot.message_handler(commands=['tozalash'])
def signals_tozalash(message):
    if message.from_user.id != ADMIN_ID:
        return bot.reply_to(message, "❌ Siz admin emassiz.")
    try:
        n = clean_signals()
        bot.send_message(message.chat.id, f"🧹 Tozalandi! {n} ta signal clean_signals.csv ga saqlandi.")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Tozalashda xatolik: {e}")

@bot.message_handler(commands=['grafik'])
def handle_girafik(message):
    try:
        if os.path.exists(BACKTEST_MATRIX):
            with open(BACKTEST_MATRIX, "rb") as photo:
                bot.send_photo(message.chat.id, photo, caption="AI Confusion Matrix")
        if os.path.exists(BACKTEST_CONFIDENCE):
            with open(BACKTEST_CONFIDENCE, "rb") as photo:
                bot.send_photo(message.chat.id, photo, caption="AI Confidence Distribution")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Grafik yuborishda xatolik: {e}")


@bot.message_handler(commands=['info'])
def handle_info(message):
    if message.from_user.id != ADMIN_ID:
        return bot.reply_to(message, "❌ Siz admin emassiz.")
    try:
        df = pd.read_csv("signals_cleaned.csv").dropna()
        df = df[df['signal'].isin(['buy', 'sell'])]
        last = df.iloc[-1]
        row = {
            'ema_fast': last['ema_fast'],
            'ema_slow': last['ema_slow'],
            'rsi': last['rsi'],
            'macd': last['macd'],
            'macd_signal': last['macd_signal'],
            'adx': last['adx'],
            'stoch_rsi': last['stoch_rsi']
        }
        pred, conf = predict_from_model(row)
        msg = f"🧠 AI Model Info:\nOxirgi signal: {last['signal']}\nBashorat: {pred.upper()}\nIshonch: {conf*100:.1f}%"
        bot.send_message(message.chat.id, msg)
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Model tahlilida xatolik: {e}")

@bot.message_handler(commands=['bashorat'])
def handle_bashorat(message):
    if message.from_user.id not in ALLOWED_USERS:
        return bot.reply_to(message, "❌ Sizga ruxsat yo‘q.")
    try:
        parts = message.text.split()
        if len(parts) != 8:
            return bot.reply_to(message, "❌ Format: /predictprice ema_fast ema_slow rsi macd macd_signal stoch_rsi adx")
        _, ema_fast, ema_slow, rsi, macd, macd_signal, stoch_rsi, adx = parts
        row = {
            'ema_fast': float(ema_fast),
            'ema_slow': float(ema_slow),
            'rsi': float(rsi),
            'macd': float(macd),
            'macd_signal': float(macd_signal),
            'stoch_rsi': float(stoch_rsi),
            'adx': float(adx)
        }
        signal, confidence = predict_from_model(row)
        bot.send_message(
            message.chat.id,
            f"🧠 Bashorat: {signal.upper()} | Ishonch: {confidence*100:.1f}%"
        )
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Xatolik: {e}")

# --- Telegram botni ishga tushurish
def start_bot_polling():
    print("🤖 Telegram bot ishlayapti...")
    while True:
        try:
            bot.infinity_polling(timeout=60, long_polling_timeout=30)
        except Exception as e:
            print(f"❌ Polling xatolik: {e}")
            time.sleep(10)

def is_paused():
    return bot_state['paused']
