# ✅ signal_logic.py – faqat indikatorlar asosida
import pandas as pd
from config import RSI_OVERBOUGHT, RSI_OVERSOLD, MIN_CONFIDENCE

def evaluate_confidence(row):
    score = 0.0
    if row['ema_fast'] > row['ema_slow']:
        score += 0.3
    if row['macd'] > row['macd_signal']:
        score += 0.3
    if RSI_OVERSOLD < row['rsi'] < RSI_OVERBOUGHT:
        score += 0.4
    return round(min(score, 1.0), 2)

def generate_signal(df: pd.DataFrame) -> tuple:
    if df is None or df.empty:
        return None, 0.0

    last = df.iloc[-1]

    ema_fast = last.get('ema_fast')
    ema_slow = last.get('ema_slow')
    rsi = last.get('rsi')
    macd = last.get('macd')
    macd_signal = last.get('macd_signal')
    adx = last.get('adx')
    stoch_rsi = last.get('stoch_rsi')

    if any(x is None or pd.isna(x) for x in [ema_fast, ema_slow, rsi, macd, macd_signal]):
        return None, 0.0

    signal = None
    if ema_fast > ema_slow and macd > macd_signal and rsi < RSI_OVERBOUGHT:
        signal = 'buy'
    elif ema_fast < ema_slow and macd < macd_signal and rsi > RSI_OVERSOLD:
        signal = 'sell'

    confidence = evaluate_confidence(last)

    extra_match = 0
    if adx is not None and not pd.isna(adx):
        if adx > 20:
            extra_match += 1
    if stoch_rsi is not None and not pd.isna(stoch_rsi):
        if signal == 'buy' and stoch_rsi < 0.8:
            extra_match += 1
        elif signal == 'sell' and stoch_rsi > 0.2:
            extra_match += 1

    if signal and extra_match >= 2:
        signal = f"KUCHLI {signal.upper()}"

    if confidence >= MIN_CONFIDENCE:
        return signal, confidence
    else:
        return None, confidence
