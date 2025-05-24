# ✅ main.py – API orqali AI'siz, rotatsion timeframe signal tekshirish (1 minutda 1 timeframe)
import time
import threading
import matplotlib.pyplot as plt
from config import SYMBOL, TIMEFRAMES, CHECK_INTERVAL
from data_fetcher import fetch_data
from indicators import apply_indicators
from signal_logic import generate_signal
from telegram_bot import send_message, send_chart, is_paused, start_bot_polling
from utils.trade import calculate_sl_tp, send_order
from logger import save_to_csv

print("✅ Bot ishga tushdi")
threading.Thread(target=start_bot_polling, daemon=True).start()

# 🔄 Timeframe indeksini boshqarish uchun
tf_index = 0

while True:
    if is_paused():
        print("⏸ Signal yuborish to‘xtatilgan.")
        time.sleep(CHECK_INTERVAL)
        continue

    # 🔁 Faqat 1ta timeframe har daqiqada tekshiriladi (rotatsion)
    tf_name = TIMEFRAMES[tf_index]
    tf_index = (tf_index + 1) % len(TIMEFRAMES)

    print(f"🔎 {SYMBOL} ({tf_name}) timeframe tekshirilmoqda...")
    df = fetch_data(symbol=SYMBOL, interval=tf_name)

    if df is None or df.empty:
        time.sleep(CHECK_INTERVAL)
        continue

    df = apply_indicators(df)
    signal, confidence = generate_signal(df)

    if signal in ['buy', 'sell', 'KUCHLI BUY', 'KUCHLI SELL']:
        price = df.iloc[-1]['close']
        sl, tp = calculate_sl_tp(df, signal.lower().replace("kuchli ", ""))

        msg = f"\n📢 {SYMBOL} | {tf_name}\nSignal: {signal}\nConfidence: {confidence*100:.0f}%\nPrice: {price:.2f}\nSL: {sl:.2f} | TP: {tp:.2f}"
        send_message(msg)

        # Grafik chizish
        plt.figure(figsize=(10, 4))
        df_tail = df.tail(50)
        plt.plot(df_tail['time'], df_tail['close'], label='Close Price')
        plt.axvline(df_tail['time'].iloc[-1], color='green' if 'BUY' in signal else 'red', linestyle='--')
        plt.title(f"{SYMBOL} - {tf_name} - {signal}")
        plt.xlabel("Time")
        plt.ylabel("Price")
        plt.grid(True)
        plt.tight_layout()
        chart_path = f"chart_{SYMBOL}_{tf_name}.png"
        plt.savefig(chart_path)
        plt.close()
        send_chart(chart_path)

        save_to_csv(SYMBOL, tf_name, signal, confidence, price)

        try:
            send_order(SYMBOL, signal.lower().replace("kuchli ", ""), 0.01, sl, tp)
        except Exception as e:
            print(f"❌ Order yuborishda xatolik: {e}")
    else:
        print(f"ℹ️ {SYMBOL} ({tf_name}): signal yo'q (Confidence: {confidence*100:.0f}%)")

    time.sleep(CHECK_INTERVAL)
