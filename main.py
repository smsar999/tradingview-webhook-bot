# -*- coding: utf-8 -*-
from fastapi import FastAPI, Request
import uvicorn

app = FastAPI()

# قاموس الكميات القصوى لكل رمز (مطابق لما في استراتيجيتك)
max_quantities = {
    "XAUUSD": 160.0,
    "NAS100": 24.0,
    "EURUSD": 460000.0,
    "USDJPY": 500000.0,
    "US30": 11.0,
    "GBPUSD": 385000.0,
    "GER40": 20.0,
    "AUDUSD": 790000.0,
    "BTCUSD": 5.0,
    "HK50": 150.0,
    "SPOTCRUDE": 7000.0,
    "ETHUSD": 180.0,
    "SOLUSD": 2450.0
}

# مسار رئيسي لاختبار الخادم
@app.get("/")
async def root():
    return {"message": "Webhook bot is running!"}

# مسار Webhook لاستقبال التنبيهات من TradingView
@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()  # استقبال بيانات JSON من TradingView
    action = data.get("action")  # استخراج نوع الأمر (buy, sell, إلخ)
    symbol = data.get("symbol")  # استخراج رمز الأداة (مثل XAUUSD)
    price = data.get("price")    # استخراج السعر
    # استخدام الكمية من القاموس بناءً على الرمز
    quantity = max_quantities.get(symbol, 0.0)

    # تنفيذ الأوامر بناءً على نوع التنبيه
    if action == "buy":
        print(f"تنفيذ أمر شراء: {quantity} من {symbol} بسعر {price}")
    elif action == "sell":
        print(f"تنفيذ أمر بيع: {quantity} من {symbol} بسعر {price}")
    elif action == "close_long":
        print(f"إغلاق صفقة طويلة لـ {symbol} بسعر {price}")
    elif action == "close_short":
        print(f"إغلاق صفقة قصيرة لـ {symbol} بسعر {price}")
    else:
        print(f"نوع أمر غير معروف: {action}")

    return {"status": "success", "data": data}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
