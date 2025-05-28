import time
from data_fetcher import fetch_data
from signal_logic import generate_signal
from telegram_bot import send_message
from logger import save_to_csv
from ai_model import predict_from_model

# 📅 Timeframe’lar va oraliqlar
TIMEFRAMES = [
    {"interval": "15min", "wait": 60},
    {"interval": "30min", "wait": 120},
    {"interval": "1h", "wait": 240},
]

SYMBOL = "XAU/USD"

print("✅ Trading loop boshlandi")

while True:
    for tf in TIMEFRAMES:
        interval = tf["interval"]
        wait = tf["wait"]

        print(f"\n🔎 {SYMBOL} ({interval}) tekshirilmoqda...")

        df = fetch_data(SYMBOL, interval)
        if df.empty:
            print("⚠️ Ma'lumot yo‘q, keyingisiga o‘tamiz.")
            time.sleep(wait)
            continue

        signal, indicators = generate_signal(df)
        if not signal:
            print("ℹ️ Signal mavjud emas.")
            time.sleep(wait)
            continue

        confidence = 0
        try:
            prediction, confidence = predict_from_model(df)
        except Exception as e:
            print(f"❌ AI model ishlamayapti: {e}")

        # Faqat ishonchli signal bo‘lsa Telegramga yuboriladi
        if confidence >= 0.6:
    message = (
        f"📊 *AI Signal*\n"
        f"🔔 {SYMBOL} ({interval})\n"
        f"📈 Signal: *{signal}*\n"
        f"🎯 Confidence: {confidence:.2f}"
    )
    send_message(message)

    price = df["close"].iloc[-1]
    save_to_csv(
        SYMBOL,
        interval,
        signal,
        confidence,
        price,
        **indicators
    )
else:
    print(f"⚠️ Confidence ({confidence:.2f}) past. Signal loglanmaydi, yuborilmaydi.")


        # Timeframe oralig‘i bo‘yicha kutish
        print(f"⏳ {wait} sekund kutilyapti...")
        time.sleep(wait)
