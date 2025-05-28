import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os

MODEL_PATH = "trained_model.pkl"
DATA_PATH = "signals_cleaned.csv"

# ✅ Modelni o‘qitish
def train_model():
    try:
        if not os.path.exists(DATA_PATH):
            print("❌ Fayl topilmadi:", DATA_PATH)
            return

        df = pd.read_csv(DATA_PATH)

        if df.empty:
            print("❌ Fayl bo‘sh! Signal mavjud emas.")
            return

        if "signal" not in df.columns:
            print("❌ 'signal' ustuni topilmadi!")
            return

        features = ["confidence", "price"]
        df = df.dropna(subset=features + ["signal"])

        if df.shape[0] < 2:
            print("❌ Kamida 2 ta signal kerak.")
            return

        X = df[features]
        y = df["signal"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        joblib.dump(model, MODEL_PATH)
        print("✅ Model o‘qitildi va saqlandi.")

        # Hisobot
        y_pred = model.predict(X_test)
        print("📊 Klassifikatsiya hisobot:")
        print(classification_report(y_test, y_pred))

    except Exception as e:
        print(f"❌ train_model() xatolik: {e}")

# ✅ Predict (bashorat) qilish
def predict_from_model(data: dict):
    """
    Parametr:
        data = {"confidence": 0.74, "price": 2350.0}
    Natija:
        "BUY", "SELL", ...
    """
    try:
        if not os.path.exists(MODEL_PATH):
            print("❌ Model mavjud emas! Avval train_model() ishga tushiring.")
            return None

        model = joblib.load(MODEL_PATH)
        X = [[data["confidence"], data["price"]]]
        prediction = model.predict(X)
        return prediction[0]

    except Exception as e:
        print(f"❌ predict_from_model() xatolik: {e}")
        return None

# ✅ AI modelni tahlil qilish (alohida komanda uchun)
def analyze_model():
    try:
        if not os.path.exists(DATA_PATH):
            print("❌ signals_cleaned.csv topilmadi")
            return

        df = pd.read_csv(DATA_PATH)

        if df.empty or "signal" not in df.columns:
            print("❌ Tahlil uchun signal mavjud emas.")
            return

        X = df[["confidence", "price"]]
        y = df["signal"]

        model = joblib.load(MODEL_PATH)
        y_pred = model.predict(X)

        print("📊 To‘liq klassifikatsiya hisobot:")
        print(classification_report(y, y_pred))

    except Exception as e:
        print(f"❌ analyze_model() xatolik: {e}")