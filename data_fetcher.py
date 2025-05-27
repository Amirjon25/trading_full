import requests
import pandas as pd
from config import TWELVE_URL
from api_manager import get_api_key

def fetch_data(symbol="XAU/USD", interval="15min", outputsize=500) -> pd.DataFrame | None:
    """
    TwelveData API orqali ma’lumot olib keladi va tayyor DataFrame qaytaradi.
    :param symbol: Masalan, "XAU/USD"
    :param interval: Masalan, "15min", "1h", "1day"
    :param outputsize: Nechta data nuqta kerak (max: 5000)
    :return: Pandas DataFrame yoki None
    """
    params = {
        "symbol": symbol,
        "interval": interval,
        "outputsize": outputsize,
        "apikey": get_api_key(),
        "format": "JSON"
    }

    try:
        response = requests.get(TWELVE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ API so‘rov xatosi: {e}")
        return None
    except ValueError:
        print("❌ JSON formatida javob olinmadi.")
        return None

    if not data or "values" not in data:
        print(f"❌ API natijasi yaroqsiz yoki 'values' yo‘q: {data}")
        return None

    try:
        df = pd.DataFrame(data["values"])
        df.rename(columns={"datetime": "time"}, inplace=True)
        df["time"] = pd.to_datetime(df["time"], errors='coerce')
        df = df.dropna(subset=["time"])  # noto‘g‘ri datetime’larni olib tashlash
        df = df.sort_values("time").reset_index(drop=True)

        numeric_cols = ["open", "high", "low", "close"]
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        df = df.dropna(subset=numeric_cols)  # noto‘g‘ri raqamlarni olib tashlash
        return df

    except Exception as e:
        print(f"❌ DataFrame yaratishda xatolik: {e}")
        return None
