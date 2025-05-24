# ✅ logger.py – signalni CSV faylga yozish
import csv
import os
from datetime import datetime

def save_to_csv(symbol, timeframe, signal, confidence, price):
    filename = "signals.csv"
    file_exists = os.path.isfile(filename)

    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)

        # Agar fayl yangi bo‘lsa, sarlavhalar yoziladi
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
