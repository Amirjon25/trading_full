import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
import os

def train_model():
    try:
        df = pd.read_csv("signals_cleaned.csv")

        if df.empty or "signal" not in df.columns:
            print("❌ signal mavjud emas yoki fayl bo‘sh!")
            return

        # Faol ustunlarni tanlash (misol uchun)
        features = ["confidence", "price"]
        df = df.dropna(subset=features + ["signal"])

        X = df[features]
        y = df["signal"]

        if len(X) < 2:
            print("❌ Model o‘qitish uchun kamida 2 ta signal kerak.")
            return

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        joblib.dump(model, "trained_model.pkl")

        print("✅ Model o‘qitildi!")
        y_pred = model.predict(X_test)
        print("📊 Klassifikatsiya hisobot:")
        print(classification_report(y_test, y_pred))

    except FileNotFoundError:
        print("❌ signals_cleaned.csv topilmadi!")
    except Exception as e:
        print(f"❌ Model o‘qitishda xatolik: {e}")

def predict_signal(confidence, price):
    try:
        if not os.path.exists("trained_model.pkl"):
            print("❌ Model mavjud emas, avval train_model() chaqiring.")
            return

        model = joblib.load("trained_model.pkl")
        prediction = model.predict([[confidence, price]])
        return prediction[0]
    except Exception as e:
        print(f"❌ Bashoratda xatolik: {e}")
        return None