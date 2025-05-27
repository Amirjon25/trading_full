# ✅ signal_logic.py – AI + Scoring asosida mukammal KUCHLI signal logikasi
import pandas as pd
from ai_model import predict_from_model
from config import RSI_OVERBOUGHT, RSI_OVERSOLD, MIN_CONFIDENCE

# 📊 Ball tizimi asosida indikatorni baholash

def score_indicators(row, signal):
    score = 0
    ema_fast = row['ema_fast']
    ema_slow = row['ema_slow']
    macd = row['macd']
    macd_signal = row['macd_signal']
    rsi = row['rsi']
    stoch_rsi = row.get('stoch_rsi', 0.5)
    adx = row.get('adx', 0)

    print(f"📊 Indikatorlar: EMA_FAST={ema_fast}, EMA_SLOW={ema_slow}, MACD={macd}, MACD_SIGNAL={macd_signal}, RSI={rsi}, STOCH_RSI={stoch_rsi}, ADX={adx}")

    if signal == "buy":
        if ema_fast > ema_slow:
            score += 1
        if macd > macd_signal:
            score += 1
        if rsi < RSI_OVERBOUGHT:
            score += 1
        if stoch_rsi <= 0.8:
            score += 1
        if adx > 20:
            score += 1

    elif signal == "sell":
        if ema_fast < ema_slow:
            score += 1
        if macd < macd_signal:
            score += 1
        if rsi > RSI_OVERSOLD:
            score += 1
        if stoch_rsi >= 0.2:
            score += 1
        if adx > 20:
            score += 1

    return score

# 🧠 Asosiy signal generator – AI + ball + confidence

def generate_signal(df: pd.DataFrame) -> tuple:
    if df is None or df.empty:
        return None, 0.0

    last = df.iloc[-1]

    try:
        pred, confidence = predict_from_model(last)
        signal = pred.lower()
    except Exception as e:
        print(f"❌ AI model ishlamayapti: {e}")
        return None, 0.0

    score = score_indicators(last, signal)

    # ✅ Minimal shartlar: AI ishonchi va indikator bal
    if confidence >= MIN_CONFIDENCE and score >= 3:

        # 💡 KUCHLI signal sharti
        adx = last.get("adx", 0)
        stoch_rsi = last.get("stoch_rsi", 0.5)
        if confidence >= 0.85 and adx > 20:
            if signal == "buy" and stoch_rsi <= 0.8:
                signal = "KUCHLI BUY"
            elif signal == "sell" and stoch_rsi >= 0.2:
                signal = "KUCHLI SELL"

        return signal, confidence
    else:
        print("⚠️ Shartlar yetarli emas.")
        return None, confidence
