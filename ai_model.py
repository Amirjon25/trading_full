# ✅ ai_model.py – signalni AI yordamida taxminlash
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib


def train_ai_model(csv_path='signals.csv'):
    df = pd.read_csv(csv_path)

    # Faqat kerakli ustunlar
    df = df.dropna()
    df = df[df['signal'].isin(['buy', 'sell'])]  # Kuchli signalni soddalashtiramiz

    df['ema_diff'] = df['ema_fast'] - df['ema_slow']
    df['macd_diff'] = df['macd'] - df['macd_signal']

    features = ['ema_diff', 'rsi', 'macd_diff', 'adx', 'stoch_rsi']
    X = df[features]
    y = df['signal']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("\n✅ Model tahlili:")
    print(classification_report(y_test, y_pred))

    joblib.dump(model, 'model.pkl')
    print("✅ AI modeli saqlandi: model.pkl")


def predict_from_model(row):
    model = joblib.load('model.pkl')
    input_data = [[
        row['ema_fast'] - row['ema_slow'],
        row['rsi'],
        row['macd'] - row['macd_signal'],
        row.get('adx', 20),
        row.get('stoch_rsi', 0.5)
    ]]
    return model.predict(input_data)[0]

# Faqat kerak bo‘lsa ishlatiladi:
# train_ai_model()
