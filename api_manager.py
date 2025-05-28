# 📦 fayl nomi: api_manager.py
import time

API_KEYS = [
    "9cdcbb93d65249b399e19a4fa2c4498f",
    "150679c2f51f4e9d8b7e891fa260dded",
    # Istasangiz, ko‘proq qo‘shing
]

key_index = 0
usage_count = 0
MAX_USAGE_PER_KEY = 790  # 800 dan sal pastda

def get_api_key():
    global key_index, usage_count

    if len(API_KEYS) == 0:
        raise ValueError("❌ API kalitlar mavjud emas.")

    if usage_count >= MAX_USAGE_PER_KEY:
        key_index = (key_index + 1) % len(API_KEYS)
        usage_count = 0
        print(f"🔄 API kalit almashtirildi: {API_KEYS[key_index][:8]}...")

    usage_count += 1
    return API_KEYS[key_index]
