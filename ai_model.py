# ✅ ai_model.py – AI modelni o‘qitish, bashorat qilish, tozalash
import pandas as pd
import joblib
from lightgbm import LGBMClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import os

from config import MODEL_FILE, CLEANED_CSV

# ✅ Modelni o‘qitish

def train_ai_model(csv_path=CLEANED_CSV):
    if not os.path.exists(csv_path):
        print(f"❌ Fayl topilmadi: {csv_path}")
        return

    df = pd.read_csv(csv_path).dropna()
    df = df[df['signal'].isin(['buy', 'sell'])]

    df['ema_diff'] = df['ema_fast'] - df['ema_slow']
    df['macd_diff'] = df['macd'] - df['macd_signal']

    features = ['ema_diff', 'rsi', 'macd_diff', 'adx', 'stoch_rsi']
    X = df[features]
    y = df['signal']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    model = LGBMClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("\n📊 AI Model Tahlili:")
    print(classification_report(y_test, y_pred))

    joblib.dump(model, MODEL_FILE)
    print(f"✅ Model saqlandi: {MODEL_FILE}")

    try:
        input_df = pd.DataFrame([X.iloc[-1]], columns=features)
        pred = model.predict(input_df)[0]
        conf = max(model.predict_proba(input_df)[0])
        print(f"🧠 AI Bashorati: {pred.upper()} | Ishonch: {conf * 100:.1f}%")
    except Exception as e:
        print(f"⚠️ Bashorat testida xatolik: {e}")


# ✅ Bashorat funksiyasi (dict formatda row kerak)
def predict_from_model(row: dict):
    if not os.path.exists(MODEL_FILE):
        raise FileNotFoundError("❌ AI modeli topilmadi. Avval train_ai_model() ni chaqiring.")

    model = joblib.load(MODEL_FILE)

    try:
        input_data = pd.DataFrame([{
            'ema_diff': row['ema_fast'] - row['ema_slow'],
            'rsi': row['rsi'],
            'macd_diff': row['macd'] - row['macd_signal'],
            'adx': row.get('adx', 20),
            'stoch_rsi': row.get('stoch_rsi', 0.5)
        }])

        pred = model.predict(input_data)[0]
        conf = max(model.predict_proba(input_data)[0])
        return pred, conf

    except Exception as e:
        print(f"❌ AI bashoratida xatolik: {e}")
        return None, 0.0


# ✅ Test rejimda ishga tushurish
if __name__ == "__main__":
    train_ai_model()
