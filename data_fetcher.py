# ✅ data_fetcher.py – API orqali ma’lumot olish (Twelve Data)
import requests
import pandas as pd
from config import API_KEY, TWELVE_URL

def fetch_data(symbol="XAU/USD", interval="15min", outputsize=500):
    """
    Twelve Data API orqali tarixiy narxlarni olish.
    """
    params = {
        "symbol": symbol,
        "interval": interval,
        "outputsize": outputsize,
        "apikey": API_KEY,
        "format": "JSON"
    }

    try:
        response = requests.get(TWELVE_URL, params=params)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"❌ API chaqiruv xatosi: {e}")
        return None

    if "values" not in data:
        print(f"❌ Ma'lumot topilmadi: {data}")
        return None

    try:
        df = pd.DataFrame(data["values"])
        df = df.rename(columns={"datetime": "time"})
        df["time"] = pd.to_datetime(df["time"])
        df = df.sort_values("time")
        df[["open", "high", "low", "close"]] = df[["open", "high", "low", "close"]].astype(float)
        return df.reset_index(drop=True)
    except Exception as e:
        print(f"❌ DataFrame tayyorlashda xatolik: {e}")
        return None
