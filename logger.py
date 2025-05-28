import csv
import os
import pandas as pd
from datetime import datetime

# 📥 Signalni signals.csv faylga yozish
def save_to_csv(symbol, timeframe, signal, confidence, price):
    """
    Signalni signals.csv faylga yozadi. Fayl yo‘q bo‘lsa, sarlavha bilan yaratadi.
    """
    filename = "signals.csv"
    file_exists = os.path.isfile(filename)

    try:
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["datetime", "symbol", "timeframe", "signal", "confidence", "price"])
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                symbol,
                timeframe,
                signal,
                round(confidence, 2),
                round(price, 2)
            ])
    except Exception as e:
        print(f"❌ CSV yozishda xatolik: {e}")

# 🧹 signals.csv faylini tozalab, AI uchun tayyorlaydi
def clean_signals(conf_threshold=0.6):
    """
    Signal logini tozalab, faqat kuchli ishonchli va to‘liq indikatorli ma’lumotlarni saqlaydi.
    Natijani signals_cleaned.csv faylga yozadi.
    """
    try:
        df = pd.read_csv("signals.csv")
        df = df.dropna()
        df = df[df["confidence"] >= conf_threshold]
        df = df[df["signal"].str.lower().isin(["buy", "sell"])]

        required_cols = [
            "datetime", "symbol", "timeframe", "signal", "confidence", "price",
            "ema_fast", "ema_slow", "rsi", "macd", "macd_signal", "adx", "stoch_rsi"
        ]
        existing_cols = [col for col in required_cols if col in df.columns]
        df = df[existing_cols]

        df.to_csv("signals_cleaned.csv", index=False)
        print(f"✅ signals_cleaned.csv saqlandi: {len(df)} ta signal")
        return len(df)

    except Exception as e:
        print(f"❌ clean_signals() xatoligi: {e}")
        return 0

# 🔁 Takroriy signalni aniqlash
def is_duplicate_signal(symbol, timeframe, signal, price, threshold=0.01):
    """
    Oxirgi yozilgan signal bilan taqqoslab, agar aynan shu turdagi signal va narx yaqin bo‘lsa – dublikat deb hisoblaydi.
    """
    try:
        df = pd.read_csv("signals.csv")
        if df.empty or len(df) < 1:
            return False

        last_row = df.iloc[-1]
        same_signal = (
            last_row["symbol"] == symbol and
            last_row["timeframe"] == timeframe and
            last_row["signal"].lower() == signal.lower() and
            abs(last_row["price"] - price) < threshold
        )
        return same_signal

    except Exception as e:
        print(f"⚠️ Dublikat tekshiruvda xatolik: {e}")
        return False
