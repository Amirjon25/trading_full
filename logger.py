import csv
import os
from datetime import datetime
import pandas as pd

# 📥 Signalni signals.csv faylga yozish
def save_to_csv(symbol, timeframe, signal, confidence, price):
    filename = "signals.csv"
    file_exists = os.path.isfile(filename)

    with open(filename, mode='a', newline='') as file:
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

# 🧹 signals.csv faylini tozalab, model uchun signals_cleaned.csv ga saqlaydi
def clean_signals(conf_threshold=0.6):
    try:
        df = pd.read_csv("signals.csv")

        if "signal" not in df.columns:
            print("❌ 'signal' ustuni signals.csv faylida topilmadi!")
            return

        df_clean = df[df["confidence"] >= conf_threshold].copy()
        df_clean.to_csv("signals_cleaned.csv", index=False)

        print(f"🧹 Tozalandi! {len(df_clean)} ta signal signals_cleaned.csv ga saqlandi.")
    except FileNotFoundError:
        print("❌ signals.csv fayli topilmadi!")
    except Exception as e:
        print(f"❌ Tozalashda xatolik: {e}")