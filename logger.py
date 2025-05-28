import csv
import os
from datetime import datetime
import pandas as pd

SIGNALS_FILE = "signals.csv"
CLEANED_FILE = "signals_cleaned.csv"

# ✅ Signalni signals.csv faylga yozish
def save_to_csv(symbol, timeframe, signal, confidence, price):
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
    Oxirgi yozilgan signal shu signal bilan bir xilmi — tekshiradi.
    """
    try:
        df = pd.read_csv(SIGNALS_FILE)
        if df.empty:
            return False
        last_row = df.iloc[-1]
        return (
            last_row["symbol"] == symbol and
            last_row["timeframe"] == timeframe and
            last_row["signal"] == signal
        )
    except Exception:
        return False

# ✅ AI uchun signalni tozalaydi va saqlaydi
def clean_signals(conf_threshold=0.6):
    try:
        df = pd.read_csv(SIGNALS_FILE)

        if "signal" not in df.columns:
            print("❌ 'signal' ustuni signals.csv faylida mavjud emas.")
            return

        df_clean = df[df["confidence"] >= conf_threshold].copy()
        df_clean.to_csv(CLEANED_FILE, index=False)

        print(f"🧹 Tozalandi! {len(df_clean)} ta signal {CLEANED_FILE} ga saqlandi.")

    except FileNotFoundError:
        print(f"❌ Fayl topilmadi: {SIGNALS_FILE}")
    except Exception as e:
        print(f"❌ Tozalashda xatolik: {e}")