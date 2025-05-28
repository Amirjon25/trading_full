import requests
import pandas as pd

API_KEY = "9cdcbb93d65249b399e19a4fa2c4498f"
BASE_URL = "https://api.twelvedata.com/time_series"

def fetch_data(symbol="XAU/USD", interval="15min", outputsize=500):
    """
    API orqali XAU/USD narxlarini olish.
    Barcha xatoliklar aniqlanadi va foydalanuvchiga tushunarli tarzda qaytariladi.
    """
    params = {
        "symbol": symbol,
        "interval": interval,
        "outputsize": outputsize,
        "apikey": API_KEY,
        "format": "JSON"
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        # 429 – API limit tugagan
        if data.get("code") == 429:
            print("❌ API limiti tugadi: kunlik limitdan oshib ketdingiz.")
            print(f"📎 {data.get('message')}")
            return pd.DataFrame()

        # API javobi noto‘g‘ri (values yo‘q)
        if "values" not in data or not data["values"]:
            print(f"⚠️ Ma'lumot yo‘q yoki bo‘sh dataframe. API natijasi: {data}")
            return pd.DataFrame()

        # Ma'lumotni DataFrame formatiga o'tkazish
        df = pd.DataFrame(data["values"])
        df["datetime"] = pd.to_datetime(df["datetime"])
        df = df.sort_values("datetime")

        # Satr turlari floatga o‘tkaziladi
        num_cols = ["open", "high", "low", "close", "volume"]
        for col in num_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        return df

    except requests.exceptions.HTTPError as e:
        if "502" in str(e):
            print("❌ TwelveData server ishlamayapti (502 Bad Gateway). Keyinroq urinib ko‘ring.")
        else:
            print(f"❌ API so‘rov xatosi: {e}")
        return pd.DataFrame()

    except Exception as e:
        print(f"❌ fetch_data() xatolik: {e}")
        return pd.DataFrame()
