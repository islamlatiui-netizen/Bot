
import requests
import pandas as pd
import ta
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ====== التوكن فقط ======
TOKEN = "PUT_YOUR_BOT_TOKEN"

SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
TIMEFRAME = "1h"

# ====== جلب البيانات ======
def get_data(symbol):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={TIMEFRAME}&limit=200"
    data = requests.get(url).json()

    df = pd.DataFrame(data, columns=[
        "time","open","high","low","close","volume",
        "ct","qav","trades","tb","tq","ignore"
    ])

    df["close"] = df["close"].astype(float)
    return df

# ====== التحليل ======
def analyze(symbol):
    df = get_data(symbol)

    df["rsi"] = ta.momentum.RSIIndicator(df["close"]).rsi()
    macd = ta.trend.MACD(df["close"])
    df["macd"] = macd.macd()
    df["signal"] = macd.macd_signal()
    df["ma50"] = df["close"].rolling(50).mean()

    last = df.iloc[-1]

    decision = "⏳ انتظار"

    if last["rsi"] < 30 and last["macd"] > last["signal"] and last["close"] > last["ma50"]:
        decision = "🚀 شراء"

    elif last["rsi"] > 70 and last["macd"] < last["signal"] and last["close"] < last["ma50"]:
        decision = "🔻 بيع"

    return f"""
📊 {symbol}

💰 السعر: {last['close']}
📉 RSI: {round(last['rsi'],2)}

📢 القرار: {decision}
"""

# ====== أوامر البوت ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 أهلا! أرسل:\n/btc\n/eth\n/sol")

async def btc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(analyze("BTCUSDT"))

async def eth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(analyze("ETHUSDT"))

async def sol(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(analyze("SOLUSDT"))

# ====== تشغيل ======
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("btc", btc))
app.add_handler(CommandHandler("eth", eth))
app.add_handler(CommandHandler("sol", sol))

print("Bot is running...")
app.run_polling()
