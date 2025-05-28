# ✅ main.py – Trading botni ishga tushirish va boshqarish
import time
import threading
import traceback
import matplotlib.pyplot as plt
from data_fetcher import fetch_data
from indicators import apply_indicators
from signal_logic import generate_signal
from logger import save_to_csv, is_duplicate_signal
from utils.trade import calculate_sl_tp, send_order
from config import SYMBOL, TIMEFRAMES, CHECK_INTERVAL
from telegram_bot import send_message, send_chart, is_paused, start_bot_polling

def run_trading_loop():
    tf_index = 0
    print("✅ Trading loop boshlandi")

    while True:
        if is_paused():
            print("⏸ Bot pauzaga olingan.")
            time.sleep(CHECK_INTERVAL)
            continue

        timeframe = TIMEFRAMES[tf_index]
        tf_index = (tf_index + 1) % len(TIMEFRAMES)

        try:
            print(f"🔎 {SYMBOL} ({timeframe}) tekshirilmoqda...")
            df = fetch_data(symbol=SYMBOL, interval=timeframe)

            if df is None or df.empty:
                print("⚠️ Ma'lumot yo'q yoki bo'sh dataframe.")
                time.sleep(CHECK_INTERVAL)
                continue

            df = apply_indicators(df)
            signal, confidence = generate_signal(df)
            last = df.iloc[-1]
            price = last['close']

            if not signal:
                print(f"ℹ️ Signal mavjud emas (Confidence: {confidence*100:.0f}%)")
                time.sleep(CHECK_INTERVAL)
                continue

            if is_duplicate_signal(SYMBOL, timeframe, signal, price):
                print("⚠️ Takroriy signal, logga yozilmadi.")
                time.sleep(CHECK_INTERVAL)
                continue

            try:
                sl, tp = calculate_sl_tp(df, signal.lower().replace("kuchli ", ""))
            except Exception as e:
                print(f"❌ SL/TP hisoblashda xato: {e}")
                continue

            msg = (
                f"📍 {SYMBOL} | {timeframe}\n"
                f"🔔 Signal: {signal}\n"
                f"🎯 Ishonch: {confidence*100:.1f}%\n"
                f"💰 Narx: {price:.2f}\n"
                f"🛡 SL: {sl:.2f} | 🎯 TP: {tp:.2f}"
            )

            try:
                df_tail = df.tail(50)
                plt.figure(figsize=(10, 4))
                plt.plot(df_tail['time'], df_tail['close'], label='Close Price')
                color = 'green' if 'BUY' in signal.upper() else 'red'
                plt.axvline(df_tail['time'].iloc[-1], color=color, linestyle='--')
                plt.title(f"{SYMBOL} - {timeframe} - {signal}")
                plt.xlabel("Time")
                plt.ylabel("Price")
                plt.grid(True)
                plt.tight_layout()

                chart_path = f"chart_{SYMBOL.replace('/', '_')}_{timeframe}.png"
                plt.savefig(chart_path)
                plt.close()
                send_chart(chart_path, caption=msg)
            except Exception as e:
                print(f"❌ Grafik chizishda xato: {e}")

            save_to_csv(
                SYMBOL, timeframe, signal, confidence, price,
                ema_fast=last.get("ema_fast"),
                ema_slow=last.get("ema_slow"),
                rsi=last.get("rsi"),
                macd=last.get("macd"),
                macd_signal=last.get("macd_signal"),
                adx=last.get("adx"),
                stoch_rsi=last.get("stoch_rsi")
            )

            try:
                send_order(SYMBOL, signal.lower().replace("kuchli ", ""), 0.01, sl, tp)
            except Exception as e:
                print(f"❌ Order yuborishda xato: {e}")

        except Exception:
            err = traceback.format_exc()
            print(f"❌ Bot siklda xato:\n{err}")
            send_message(f"❌ Botda xatolik:\n{err}")

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    print("🤖 Telegram bot ishga tushmoqda...")
    threading.Thread(target=start_bot_polling, daemon=True).start()
    run_trading_loop()
