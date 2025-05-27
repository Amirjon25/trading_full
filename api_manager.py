import time
import random

# 🔐 API kalitlar (xavfsizlik uchun .env faylga o‘tkazish tavsiya etiladi)
API_KEYS = [
    "9cdcbb93d65249b399e19a4fa2c4498f",
    "150679c2f51f4e9d8b7e891fa260dded",
    # "qo‘shimcha kalitlar bo‘lsa shu yerga yozing"
]

# 🔁 Rotatsiya sozlamalari
key_index = 0
usage_count = 0
MAX_USAGE_PER_KEY = 790  # API limit yaqinlashganda key almashtiriladi

# 🧠 API kalit olish funksiyasi
def get_api_key():
    """
    Har chaqirilganda avtomatik tarzda kalitni qaytaradi.
    Agar kalit limitga yetgan bo‘lsa, keyingi kalitga o‘tadi.
    """
    global key_index, usage_count

    if len(API_KEYS) == 0:
        raise ValueError("❌ API kalitlar ro‘yxati bo‘sh.")

    if usage_count >= MAX_USAGE_PER_KEY:
        key_index = (key_index + 1) % len(API_KEYS)
        usage_count = 0
        print(f"🔄 API kalit almashtirildi: {API_KEYS[key_index][:8]}...")

    usage_count += 1
    return API_KEYS[key_index]

# 🧪 Test rejimi
if __name__ == "__main__":
    print("🧪 API kalit test:")
    for i in range(5):
        print(f"{i+1}) {get_api_key()}")
        time.sleep(0.5)
