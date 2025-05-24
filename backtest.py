# ✅ backtest.py (CSV signal tarixiga asoslangan aniqlik tahlili)
import pandas as pd

CSV_FILE = "signals.csv"
TP_PIPS = 100  # taxminiy Take Profit
SL_PIPS = 50   # taxminiy Stop Loss


def simulate_trade(signal_row):
    direction = signal_row['signal']
    entry = signal_row['price']
    if direction == 'buy':
        tp = entry + TP_PIPS * 0.1  # PIP konversiyasi
        sl = entry - SL_PIPS * 0.1
        result = 'win' if tp >= entry * 1.01 else 'loss'
    elif direction == 'sell':
        tp = entry - TP_PIPS * 0.1
        sl = entry + SL_PIPS * 0.1
        result = 'win' if tp <= entry * 0.99 else 'loss'
    else:
        result = 'skip'
    return result


def backtest():
    try:
        df = pd.read_csv(CSV_FILE)
        results = {'win': 0, 'loss': 0, 'skip': 0}

        for _, row in df.iterrows():
            result = simulate_trade(row)
            results[result] += 1

        total = results['win'] + results['loss']
        accuracy = results['win'] / total * 100 if total > 0 else 0

        print("📊 Backtest natijasi:")
        print(f"✅ G‘alabalar: {results['win']}")
        print(f"❌ Yo‘qotishlar: {results['loss']}")
        print(f"🕓 O‘tkazib yuborilgan: {results['skip']}")
        print(f"🎯 Aniqlik: {accuracy:.2f}%")

    except Exception as e:
        print(f"❌ Backtest xatoligi: {e}")


if __name__ == "__main__":
    backtest()
