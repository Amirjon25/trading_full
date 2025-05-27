# ✅ backtest_ai.py – AI modelning aniqligini test va vizual tahlil qilish

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from ai_model import predict_from_model
from config import CLEANED_CSV, BACKTEST_MATRIX, BACKTEST_CONFIDENCE

def run_backtest():
    try:
        # 📥 Ma'lumotlarni yuklash
        df = pd.read_csv(CLEANED_CSV).dropna()
        df = df[df['signal'].isin(['buy', 'sell'])]  # Faqat kerakli signal turlari

        y_true, y_pred, confidence_scores = [], [], []

        print(f"🔎 {len(df)} ta signal ustida test bajarilmoqda...")

        # 🔄 Har bir signal ustida AI bashoratini test qilish
        for _, row in df.iterrows():
            try:
                pred, conf = predict_from_model(row)
                y_true.append(row['signal'])
                y_pred.append(pred)
                confidence_scores.append(conf)
            except Exception as e:
                print(f"⚠️ Satr tashlab o‘tildi: {e}")

        # 🧾 To‘liq klassifikatsiya hisoboti
        print("\n📊 AI Backtest Hisoboti:")
        print(classification_report(y_true, y_pred))
        acc = accuracy_score(y_true, y_pred)
        print(f"🔍 Umumiy aniqlik: {acc * 100:.2f}%")

        # 📈 Confusion Matrix
        cm = confusion_matrix(y_true, y_pred, labels=['buy', 'sell'])
        plt.figure(figsize=(6, 5))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                    xticklabels=['Buy', 'Sell'], yticklabels=['Buy', 'Sell'])
        plt.title("Confusion Matrix – AI Bashorati")
        plt.xlabel("Model Bashorati")
        plt.ylabel("Haqiqiy Signal")
        plt.tight_layout()
        plt.savefig(BACKTEST_MATRIX)
        plt.close()
        print(f"✅ Confusion matrix saqlandi: {BACKTEST_MATRIX}")

        # 📉 Confidence tarqalishi
        plt.figure(figsize=(6, 4))
        sns.histplot(confidence_scores, bins=20, kde=True, color='green')
        plt.title("Confidence Score Tarqalishi")
        plt.xlabel("AI Ishonchlilik (0–1)")
        plt.ylabel("Tartib")
        plt.tight_layout()
        plt.savefig(BACKTEST_CONFIDENCE)
        plt.close()
        print(f"✅ Confidence grafigi saqlandi: {BACKTEST_CONFIDENCE}")

    except Exception as e:
        print(f"❌ Backtest xatoligi: {e}")

# 🧪 Test sifatida ishga tushirish
if __name__ == "__main__":
    run_backtest()
