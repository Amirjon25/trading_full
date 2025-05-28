from api_manager import get_api_key
from telegram_bot import handle_api_error
import requests
import pandas as pd

BASE_URL = "https://api.twelvedata.com/time_series"

def fetch_data(symbol="XAU/USD", interval="15min", outputsize=500):
    for attempt in range(2):  # har bir so‘rovni 2 marta har xil kalit bilan urinib ko‘ramiz
        api_key = get_api_key()

        params = {
            "symbol": symbol,
            "interval": interval,
            "outputsize": outputsize,
            "apikey": api_key,
            "format": "JSON"
        }

        try:
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

            if data.get("code") == 429:
                print(f"⚠️ API limiti tugadi: {api_key[:8]}...")
                handle_api_error(f"API kalit limiti tugadi: {api_key[:8]}...")
                continue  # keyingi kalitga o‘tish

            if "values" not in data or not data["values"]:
                msg = f"⚠️ Ma'lumot yo‘q. JSON: {data}"
                print(msg)
                handle_api_error(msg)
                return pd.DataFrame()

            # JSON'dan DataFrame
            df = pd.DataFrame(data["values"])
            df["datetime"] = pd.to_datetime(df["datetime"])
            df = df.sort_values("datetime")

            for col in ["open", "high", "low", "close", "volume"]:
                df[col] = pd.to_numeric(df[col], errors="coerce")

            return df

        except requests.exceptions.HTTPError as e:
            msg = f"❌ HTTP xatolik: {e}"
            print(msg)
            handle_api_error(msg)

        except Exception as e:
            msg = f"❌ Umumiy xatolik: {e}"
            print(msg)
            handle_api_error(msg)

    print("❌ Barcha API kalitlar limitda yoki xato.")
    return pd.DataFrame()
