import requests
import telebot
import pandas as pd
import ta
import time
from datetime import datetime

TOKEN = "ВСТАВЬ_СЮДА_ТОКЕН"
CHANNEL_ID = "@username_канала"

bot = telebot.TeleBot(TOKEN)

def get_gold_data():
    url = "https://query1.finance.yahoo.com/v7/finance/download/GC=F?period1=0&period2=9999999999&interval=5m&events=history"
    df = pd.read_csv(url)
    return df.tail(200)

def check_signal():
    df = get_gold_data()

    df['ema50'] = ta.trend.EMAIndicator(df['Close'], 50).ema_indicator()
    df['ema200'] = ta.trend.EMAIndicator(df['Close'], 200).ema_indicator()
    df['rsi'] = ta.momentum.RSIIndicator(df['Close'], 14).rsi()

    last = df.iloc[-1]

    price = round(last['Close'],2)
    ema50 = last['ema50']
    ema200 = last['ema200']
    rsi = last['rsi']

    now = datetime.now().strftime("%d.%m.%Y | %H:%M")

    if ema50 > ema200 and rsi < 35:
        sl = price - 7
        tp = price + 15
        text = f"""
💎 GOLD AUTO SIGNAL

📊 XAUUSD
📈 BUY

🎯 Entry: {price}
🛑 SL: {round(sl,2)}
💰 TP: {round(tp,2)}

🧠 Strategy: EMA + RSI
🕒 {now}
"""
        bot.send_message(CHANNEL_ID, text)

    elif ema50 < ema200 and rsi > 65:
        sl = price + 7
        tp = price - 15
        text = f"""
💎 GOLD AUTO SIGNAL

📊 XAUUSD
📉 SELL

🎯 Entry: {price}
🛑 SL: {round(sl,2)}
💰 TP: {round(tp,2)}

🧠 Strategy: EMA + RSI
🕒 {now}
"""
        bot.send_message(CHANNEL_ID, text)

print("Bot started...")

while True:
    try:
        check_signal()
        time.sleep(300)
    except:
        time.sleep(300)
