# ✅ config.py (Twelve Data versiyasi)
import os
from dotenv import load_dotenv

load_dotenv()

# 📡 API va Telegram sozlamalar
API_KEY = os.getenv("API_KEY") or "9cdcbb93d65249b399e19a4fa2c4498f"
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

# 🕒 Timeframe konfiguratsiyasi
TIMEFRAMES = ["15min", "30min", "1h"]

SYMBOL = "XAU/USD"
CHECK_INTERVAL = 60  # har 1 daqiqa

# 📈 Indikator sozlamalari
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
EMA_FAST_PERIOD = 9
EMA_SLOW_PERIOD = 21
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
MIN_CONFIDENCE = 0.6

# 🌐 Twelve Data API manzili
TWELVE_URL = "https://api.twelvedata.com/time_series"

# 📁 Signal log fayli
CSV_LOG = "signals.csv"
