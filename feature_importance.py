# ✅ feature_importance.py – Modelda indikator og‘irliklarini chizish
import pandas as pd
import joblib
import matplotlib.pyplot as plt

# Modelni yuklaymiz
model = joblib.load("model.pkl")

# Indikatorlar ro‘yxati
features = ['ema_diff', 'rsi', 'macd_diff', 'adx', 'stoch_rsi']
importances = model.feature_importances_

# Grafik chizish
plt.figure(figsize=(7, 4))
plt.barh(features, importances)
plt.title(" AI Model – Feature Importance")
plt.xlabel("Muhimlik darajasi")
plt.grid(True)
plt.tight_layout()
plt.savefig("feature_importance.png")
plt.show()
