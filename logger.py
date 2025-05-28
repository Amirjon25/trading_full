import csv
import os
import pandas as pd
from datetime import datetime, timedelta

# 📥 Signalni signals.csv faylga yozish
def save_to_csv(symbol, timeframe, signal, confidence, price,
                ema_fast=None, ema_slow=None, rsi=None,
                macd=None, macd_signal=None, adx=None, stoch_rsi=None):
    filename = "signals.csv"
    file_exists = os.path.isfile(filename)

    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow([
                "datetime", "symbol", "timeframe", "signal", "confidence", "price",
                "ema_fast", "ema_slow", "rsi",
                "macd", "macd_signal", "adx", "stoch_rsi"
            ])
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            symbol,
            timeframe,
            signal,
            round(confidence, 2),
            round(price, 2),
            ema_fast, ema_slow, rsi,
            macd, macd_signal, adx, stoch_rsi
        ])

# 🧹 signals.csv faylini tozalab, AI uchun tayyorlaydi
def clean_signals(conf_threshold=0.6):
    try:
        df = pd.read_csv("signals.csv")
        if "confidence" not in df.columns:
            print("❌ signals.csv faylida 'confidence' ustuni yo‘q.")
            return 0

        # Faqat kerakli confidence'dan yuqori signal
        cleaned_df = df[df["confidence"] >= conf_threshold]
        cleaned_df.to_csv("signals_cleaned.csv", index=False)
        print(f"🧹 Tozalandi! {len(cleaned_df)} ta signal clean_signals.csv ga saqlandi.")
        return len(cleaned_df)

    except FileNotFoundError:
        print("❌ signals.csv fayli topilmadi.")
        return 0
    except Exception as e:
        print(f"❌ clean_signals() xatolik: {e}")
        return 0

# 🔁 Takroriy signalni tekshirish (ixtiyoriy foydalanish)
def is_duplicate_signal(symbol, signal, timeframe, minutes_gap=30):
    try:
        df = pd.read_csv("signals.csv")
        df["datetime"] = pd.to_datetime(df["datetime"])

        latest = df[
            (df["symbol"] == symbol) &
            (df["signal"] == signal) &
            (df["timeframe"] == timeframe)
        ].sort_values("datetime", ascending=False)

        if not latest.empty:
            last_time = latest.iloc[0]["datetime"]
            now = datetime.now()
            delta = now - pd.to_datetime(last_time)
            if delta < timedelta(minutes=minutes_gap):
                print(f"⚠️ Takroriy signal (oldingi {delta.seconds // 60} daqiqa oldin).")
                return True

        return False
    except Exception as e:
        print(f"❌ is_duplicate_signal() xatolik: {e}")
        return False
