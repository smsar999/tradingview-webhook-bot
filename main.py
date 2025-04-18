# -*- coding: utf-8 -*-
from fastapi import FastAPI, Request
import uvicorn
import requests

app = FastAPI()

# قاموس الكميات القصوى لكل رمز
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

# إعدادات Telegram
TELEGRAM_BOT_TOKEN = "your_bot_token"  # استبدل بالـ Token من @BotFather
TELEGRAM_CHAT_ID = "your_chat_id"  # استبدل بالـ Chat ID بتاعك

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print(f"تم إرسال رسالة إلى Telegram: {message}")
        else:
            print(f"خطأ في إرسال الرسالة إلى Telegram: {response.text}")
    except Exception as e:
        print(f"خطأ في إرسال الرسالة إلى Telegram: {e}")

# مسار رئيسي لاختبار الخادم
@app.get("/")
async def root():
    return {"message": "Webhook bot is running!"}

@app.head("/")
async def head_root():
    return {"message": "Webhook bot is running!"}

# مسار Webhook لاستقبال التنبيهات من TradingView
@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()  # استقبال بيانات JSON من TradingView
    action = data.get("action")  # استخراج نوع الأمر (buy, sell, إلخ)
    symbol = data.get("symbol")  # استخراج رمز الأداة (مثل XAUUSD)
    price = data.get("price")    # استخراج السعر
    quantity = max_quantities.get(symbol, 0.0)  # استخراج الكمية

    # إعداد رسالة الأمر
    if action == "buy":
        message = f"تنفيذ أمر شراء: {quantity} من {symbol} بسعر {price}"
    elif action == "sell":
        message = f"تنفيذ أمر بيع: {quantity} من {symbol} بسعر {price}"
    elif action == "close_long":
        message = f"إغلاق صفقة طويلة لـ {symbol} بسعر {price}"
    elif action == "close_short":
        message = f"إغلاق صفقة قصيرة لـ {symbol} بسعر {price}"
    else:
        message = f"نوع أمر غير معروف: {action}"

    # طباعة الأمر في السجلات
    print(message)

    # إرسال الأمر إلى Telegram
    send_telegram_message(message)

    return {"status": "success", "data": data}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
