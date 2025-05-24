# ✅ utils/trade.py – SL/TP hisoblash va order yuborish (mock)
import random

def calculate_sl_tp(df, signal):
    last_price = df.iloc[-1]['close']
    atr = df['high'].rolling(window=14).max() - df['low'].rolling(window=14).min()
    atr = atr.iloc[-1] if not atr.empty else 1.0

    sl_buffer = 0.5  # xavfsizlik buferi
    atr += sl_buffer

    if signal == 'buy':
        sl = last_price - atr
        tp = last_price + atr * 2
    else:
        sl = last_price + atr
        tp = last_price - atr * 2

    return round(sl, 2), round(tp, 2)

def send_order(symbol, signal, lot, sl, tp):
    # Hozircha faqat test rejimi uchun ishlaydi
    print(f"✅ MOCK ORDER SENT: {symbol} | {signal.upper()} | Lot: {lot} | SL: {sl} | TP: {tp}")
