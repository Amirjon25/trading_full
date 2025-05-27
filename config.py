# ✅ config.py – Konfiguratsiya parametrlarini markazlashtirish
import os
from dotenv import load_dotenv

# 🔄 .env fayldan token va IDlarni yuklaymiz
load_dotenv()

# --- Telegram va API kalitlari ---
API_KEY = os.getenv("API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# --- Trading sozlamalari ---
SYMBOL = "XAU/USD"
TIMEFRAMES = ["15min", "30min", "1h"]  # Foydalaniladigan timeframe’lar
CHECK_INTERVAL = 60  # sekundlarda tekshirish oraliği

# --- Indikator parametrlar ---
RSI_OVERBOUGHT = 70.0
RSI_OVERSOLD = 30.0
EMA_FAST_PERIOD = 9
EMA_SLOW_PERIOD = 21
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

# --- AI signal minimal ishonchlilik ---
MIN_CONFIDENCE = 0.6  # Asosiy model uchun
HIGH_CONFIDENCE = 0.85  # KUCHLI signal uchun

# --- Backtest va AI baholash uchun ---
BACKTEST_MATRIX = "backtest_confusion_matrix.png"
BACKTEST_CONFIDENCE = "backtest_confidence.png"

# --- Fayllar nomi va joylashuvi ---
CSV_LOG = "signals.csv"
CLEANED_CSV = "signals_cleaned.csv"
MODEL_FILE = "model.pkl"
ALLOWED_USERS_FILE = "allowed_users.json"
TWELVE_URL = "https://api.twelvedata.com/time_series"
