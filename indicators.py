import pandas as pd
import numpy as np

def apply_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # --- EMA (Exponential Moving Average)
    df['ema_fast'] = df['close'].ewm(span=9, adjust=False).mean()
    df['ema_slow'] = df['close'].ewm(span=21, adjust=False).mean()

    # --- RSI (Relative Strength Index)
    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / (avg_loss + 1e-9)
    df['rsi'] = 100 - (100 / (1 + rs))

    # --- Stochastic RSI
    min_rsi = df['rsi'].rolling(window=14).min()
    max_rsi = df['rsi'].rolling(window=14).max()
    df['stoch_rsi'] = (df['rsi'] - min_rsi) / (max_rsi - min_rsi + 1e-9)

    # --- MACD (Moving Average Convergence Divergence)
    ema12 = df['close'].ewm(span=12, adjust=False).mean()
    ema26 = df['close'].ewm(span=26, adjust=False).mean()
    df['macd'] = ema12 - ema26
    df['macd_signal'] = df['macd'].ewm(span=9, adjust=False).mean()

    # --- Bollinger Bands
    df['bollinger_middle'] = df['close'].rolling(window=20).mean()
    rolling_std = df['close'].rolling(window=20).std()
    df['bollinger_upper'] = df['bollinger_middle'] + 2 * rolling_std
    df['bollinger_lower'] = df['bollinger_middle'] - 2 * rolling_std

    # --- ATR (Average True Range)
    df['previous_close'] = df['close'].shift(1)
    high_low = df['high'] - df['low']
    high_close = (df['high'] - df['previous_close']).abs()
    low_close = (df['low'] - df['previous_close']).abs()
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    df['atr'] = tr.rolling(window=14).mean()

    # --- ADX (Average Directional Index)
    up_move = df['high'].diff()
    down_move = df['low'].diff().abs()
    plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0.0)
    minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0.0)

    tr14 = tr.rolling(window=14).mean()
    plus_di = 100 * pd.Series(plus_dm).rolling(window=14).mean() / (tr14 + 1e-9)
    minus_di = 100 * pd.Series(minus_dm).rolling(window=14).mean() / (tr14 + 1e-9)
    dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di + 1e-9)
    df['adx'] = dx.rolling(window=14).mean()

    # Tozalash va indeksni tiklash
    df.drop(columns=['previous_close'], inplace=True)
    return df.dropna().reset_index(drop=True)
