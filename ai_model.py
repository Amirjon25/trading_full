import os
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

MODEL_PATH = "trained_model.pkl"
DATA_PATH = "signals_cleaned.csv"

# ✅ Modelni o‘qitish (train_ai_model)
def train_ai_model():
    try:
        if not os.path.exists(DATA_PATH):
            print(f"❌ Fayl topilmadi: {DATA_PATH}")
            return

        df = pd.read_csv(DATA_PATH)

        if df.empty or "signal" not in df.columns:
            print("❌ Fayl bo‘sh yoki 'signal' ustuni mavjud emas.")
            return

        # Foydalaniladigan ustunlar
        df = df.dropna(subset=["confidence", "price", "signal"])
        if df.shape[0] < 2:
            print("❌ Kamida 2 ta signal kerak.")
            return

        X = df[["confidence", "price"]]
        y = df["signal"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        joblib.dump(model, MODEL_PATH)
        print("✅ Model o‘qitildi va saqlandi!")

        y_pred = model.predict(X_test)
        print("📊 Klassifikatsiya hisobot:")
        print(classification_report(y_test, y_pred))

    except Exception as e:
        print(f"❌ train_ai_model() xatolik: {e}")

# ✅ AI model orqali signal bashorati (predict_from_model)
def predict_from_model(data: dict):
    """
    Parametr:
        data = {"confidence": 0.73, "price": 2349.0}
    Natija:
        ("BUY", 0.83)
    """
    try:
        if not os.path.exists(MODEL_PATH):
            print("❌ Model mavjud emas. Avval train_ai_model() chaqiring.")
            return None

        model = joblib.load(MODEL_PATH)
        X = [[data["confidence"], data["price"]]]
        prediction = model.predict(X)
        proba = model.predict_proba(X)

        confidence_score = max(proba[0])  # Model ishonch darajasi
        return prediction[0], round(confidence_score, 2)

    except Exception as e:
        print(f"❌ predict_from_model() xatolik: {e}")
        return None