import csv
import os
from datetime import datetime
import pandas as pd

# Fayl nomlari
SIGNALS_FILE = "signals.csv"
CLEANED_FILE = "signals_cleaned.csv"

# ✅ Signalni CSV faylga yozish
def save_to_csv(symbol, timeframe, signal, confidence, price):
    """
    signal: 'BUY', 'SELL', 'KUCHLI BUY', 'KUCHLI SELL'
    """
    file_exists = os.path.isfile(SIGNALS_FILE)

    with open(SIGNALS_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["timestamp", "symbol", "timeframe", "signal", "confidence", "price"])
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            symbol,
            timeframe,
            signal,
            round(confidence, 2),
            round(price, 2)
        ])
    print(f"✅ Signal yozildi: {symbol} | {timeframe} | {signal} | {confidence}")

# ✅ Takroriy signalni tekshiradi
def is_duplicate_signal(symbol, timeframe, signal):
    """
    signals.csv faylida oxirgi signal aynan shu symbol, timeframe va signal bilan bir xilmi — tekshiradi.
    """
    try:
        if not os.path.exists(SIGNALS_FILE):
            return False

        df = pd.read_csv(SIGNALS_FILE)
        if df.empty:
            return False

        last_row = df.iloc[-1]
        return (
            last_row["symbol"] == symbol and
            last_row["timeframe"] == timeframe and
            last_row["signal"] == signal
        )

    except Exception as e:
        print(f"❌ is_duplicate_signal() xatolik: {e}")
        return False

# ✅ AI uchun signalni tozalaydi
def clean_signals(conf_threshold=0.6):
    """
    `confidence` qiymati conf_threshold dan yuqori bo‘lgan signalni ajratib alohida faylga yozadi
    """
    try:
        if not os.path.exists(SIGNALS_FILE):
            print("❌ signals.csv fayli mavjud emas.")
            return

        df = pd.read_csv(SIGNALS_FILE)

        if "signal" not in df.columns:
            print("❌ 'signal' ustuni signals.csv faylida mavjud emas.")
            return

        df_clean = df[df["confidence"] >= conf_threshold].copy()

        if df_clean.empty:
            print("⚠️ Tozalashdan so‘ng hech qanday signal qolmadi.")
        else:
            df_clean.to_csv(CLEANED_FILE, index=False)
            print(f"🧹 {len(df_clean)} ta signal tozalandi va {CLEANED_FILE} faylga yozildi.")

    except Exception as e:
        print(f"❌ clean_signals() xatolik: {e}")