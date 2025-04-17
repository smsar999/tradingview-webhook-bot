# -*- coding: utf-8 -*-
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# الحد الأقصى للأحجام حسب الرموز (حسب شروط المسابقة)
MAX_LOT_SIZES = {
    "XAUUSD": 5,
    "NAS100": 30,
    "SPX500": 30,
    "DE40": 10,
    "GER40": 10,
    "US30": 30,
    "BTCUSD": 1,
    "ETHUSD": 10,
    "USDJPY": 100,
    "EURUSD": 100,
    "GBPUSD": 100,
    "AUDUSD": 100,
    "NZDUSD": 100,
    "USDCHF": 100,
    "USDCAD": 100,
    "USOUSD": 50,
    "UKOUSD": 50
}

@app.route('/', methods=['POST'])
def webhook():
    data = request.json
    print("🚀 Webhook received:", data)

    action = data.get('action')
    symbol = data.get('symbol')
    quantity = float(data.get('quantity', 0))
    price = float(data.get('price', 0))

    # التحقق من الرمز والحجم
    max_size = MAX_LOT_SIZES.get(symbol)
    if not max_size:
        return jsonify({"status": "error", "message": f"رمز غير مدعوم: {symbol}"}), 400
    if quantity > max_size:
        return jsonify({"status": "error", "message": f"الحجم {quantity} أكبر من الحد الأقصى {max_size} للرمز {symbol}"}), 400

    if action in ['buy', 'sell']:
        simulate_trade(action, symbol, quantity, price)
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "error", "message": "إجراء غير معروف"}), 400

def simulate_trade(action, symbol, quantity, price):
    print(f"\n✅ تنفيذ {action.upper()} لـ {symbol}")
    print(f"📦 الحجم: {quantity}")
    print(f"💰 السعر: {price}")
    print(f"⛔ وقف الخسارة: {calculate_stop_loss(price, action)}")
    print(f"🎯 الهدف: {calculate_take_profit(price, action)}")

def calculate_stop_loss(price, order_type):
    return round(price * 0.99, 2) if order_type == 'buy' else round(price * 1.01, 2)

def calculate_take_profit(price, order_type):
    return round(price * 1.02, 2) if order_type == 'buy' else round(price * 0.98, 2)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
