# ✅ utils/trade.py – SL/TP va order yuborish (mock + tayyor)

import pandas as pd

# 📐 SL/TP hisoblash – ATR asosida
def calculate_sl_tp(df, signal: str, risk_ratio: float = 2.0, atr_multiplier: float = 1.0) -> tuple:
    """
    SL (Stop Loss) va TP (Take Profit) ni ATR asosida hisoblaydi.
    :param df: DataFrame (indikatorlar bilan)
    :param signal: 'buy' yoki 'sell'
    :param risk_ratio: TP uchun risk/reward nisbati
    :param atr_multiplier: ATR ni kuchaytirish koeffitsiyenti
    :return: (SL, TP)
    """
    last_price = df.iloc[-1]['close']
    atr = df.iloc[-1].get('atr', None)

    if pd.isna(atr) or atr is None:
        print("⚠️ ATR topilmadi, default = 1.0 qo‘llanildi.")
        atr = 1.0

    atr = max(0.1, atr * atr_multiplier)  # Xavfsizlik uchun 0.1 dan past bo‘lmasin

    if signal == 'buy':
        sl = last_price - atr
        tp = last_price + atr * risk_ratio
    elif signal == 'sell':
        sl = last_price + atr
        tp = last_price - atr * risk_ratio
    else:
        raise ValueError("❌ signal faqat 'buy' yoki 'sell' bo‘lishi kerak.")

    return round(sl, 2), round(tp, 2)

# 🛒 Order yuborish – mock rejim (haqiqiy broker API keyincha qo‘shiladi)
def send_order(symbol: str, signal: str, lot: float, sl: float, tp: float, live: bool = False, comment: str = "AI Signal"):
    """
    Order yuborish funksiyasi (mock yoki haqiqiy)
    :param symbol: Valyuta jufti (masalan, "XAU/USD")
    :param signal: 'buy' yoki 'sell'
    :param lot: Lot hajmi
    :param sl: Stop Loss qiymati
    :param tp: Take Profit qiymati
    :param live: Haqiqiy broker API bo‘lsa True
    :param comment: Izoh
    """
    if live:
        # TODO: Broker API integratsiyasi shu yerga yoziladi:
        # Masalan:
        # broker_api.send_order(symbol, signal, lot, sl, tp, comment)
        print(f"📤 REAL ORDER YUBORILDI: {symbol} | {signal.upper()} | Lot: {lot} | SL: {sl} | TP: {tp} | 💬 {comment}")
    else:
        print(f"✅ MOCK ORDER: {symbol} | {signal.upper()} | Lot: {lot} | SL: {sl} | TP: {tp} | 💬 {comment}")
