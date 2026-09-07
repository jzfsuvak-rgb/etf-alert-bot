import os
import requests
import yfinance as yf
from flask import Flask

app = Flask(__name__)

# ==================== KONFIGURÁCIA ====================
TELEGRAM_TOKEN = "8888485121:AAEvtckgjk8l9eO-Zb2oF2ohUEjD-z0W7Xg"
CHAT_ID = "5366772205"

INSTRUMENTS = {
    "GC=F": 2.0,       # Zlato
    "SI=F": 0.20,      # Striebro
    "ZEC-USD": 5.0,    # Zcash
    "^GDAXI": 20.0,    # GER40
    "^NDX": 20.0,      # NAS100
    "BZ=F": 0.50,      # Ropa
    "HG=F": 0.05       # Med
}
# ======================================================

@app.route('/')
def home():
    for ticker, threshold in INSTRUMENTS.items():
        try:
            data = yf.Ticker(ticker)
            history = data.history(period="1d")
            if not history.empty:
                current_price = history['Close'].iloc[-1]
                url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
                payload = {"chat_id": CHAT_ID, "text": f"🔎 Kontrola: {ticker} je momentálne za {round(current_price, 2)}"}
                requests.post(url, json=payload)
        except Exception as e:
            print(f"Chyba pre {ticker}: {e}")
            
    return "Kontrola trhov úspešne spustená!", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
