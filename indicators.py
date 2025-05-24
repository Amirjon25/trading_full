import pandas as pd

def apply_indicators(df: pd.DataFrame) -> pd.DataFrame:
    # EMA
    df['ema_fast'] = df['close'].ewm(span=9, adjust=False).mean()
    df['ema_slow'] = df['close'].ewm(span=21, adjust=False).mean()

    # RSI
    delta = df['close'].diff()
    gain = delta.clip(lower=0).rolling(window=14).mean()
    loss = -delta.clip(upper=0).rolling(window=14).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))

    # MACD
    ema12 = df['close'].ewm(span=12, adjust=False).mean()
    ema26 = df['close'].ewm(span=26, adjust=False).mean()
    df['macd'] = ema12 - ema26
    df['macd_signal'] = df['macd'].ewm(span=9, adjust=False).mean()

    # ✅ Bollinger Bands
    df['bollinger_middle'] = df['close'].rolling(window=20).mean()
    std = df['close'].rolling(window=20).std()
    df['bollinger_upper'] = df['bollinger_middle'] + (std * 2)
    df['bollinger_lower'] = df['bollinger_middle'] - (std * 2)

    # ✅ ATR (Average True Range)
    df['tr'] = df[['high', 'low', 'close']].apply(
        lambda row: max(row['high'] - row['low'], abs(row['high'] - row['close']), abs(row['low'] - row['close'])),
        axis=1
    )
    df['atr'] = df['tr'].rolling(window=14).mean()

    # ✅ ADX
    df['plus_dm'] = df['high'].diff()
    df['minus_dm'] = df['low'].diff().abs()
    df['plus_dm'] = df['plus_dm'].where(df['plus_dm'] > df['minus_dm'], 0.0)
    df['minus_dm'] = df['minus_dm'].where(df['minus_dm'] > df['plus_dm'], 0.0)

    tr = df['tr']
    df['plus_di'] = 100 * (df['plus_dm'].rolling(window=14).mean() / tr.rolling(window=14).mean())
    df['minus_di'] = 100 * (df['minus_dm'].rolling(window=14).mean() / tr.rolling(window=14).mean())
    dx = 100 * (abs(df['plus_di'] - df['minus_di']) / (df['plus_di'] + df['minus_di']))
    df['adx'] = dx.rolling(window=14).mean()

    return df
