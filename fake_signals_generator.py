# ✅ fake_signals_generator.py – test uchun signals.csv to‘ldiradi
import csv
import random
from datetime import datetime

FILENAME = "signals.csv"

def generate_signal_row():
    base_time = datetime.now()
    signal = random.choice(["buy", "sell"])
    confidence = round(random.uniform(0.6, 0.95), 2)
    price = round(random.uniform(1900, 2000), 2)

    ema_fast = price + random.uniform(-1, 1)
    ema_slow = price + random.uniform(-1, 1)
    macd = random.uniform(-2, 2)
    macd_signal = macd + random.uniform(-0.5, 0.5)
    rsi = random.uniform(20, 80)
    adx = random.uniform(10, 35)
    stoch_rsi = random.uniform(0, 1)

    return [
        base_time.strftime("%Y-%m-%d %H:%M:%S"),
        "XAU/USD",
        "15min",
        signal,
        confidence,
        price,
        round(ema_fast, 4),
        round(ema_slow, 4),
        round(macd, 4),
        round(macd_signal, 4),
        round(rsi, 2),
        round(adx, 2),
        round(stoch_rsi, 3)
    ]

def generate_fake_signals(n=50):
    with open(FILENAME, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            "datetime", "symbol", "timeframe", "signal", "confidence", "price",
            "ema_fast", "ema_slow", "macd", "macd_signal", "rsi", "adx", "stoch_rsi"
        ])

        for _ in range(n):
            writer.writerow(generate_signal_row())

    print(f"✅ {n} ta test signal yaratildi → {FILENAME}")

if __name__ == "__main__":
    generate_fake_signals(100)
