import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from tradingview_ta import TA_Handler, Interval

TOKEN = os.getenv("BOT_TOKEN")

# دالة التحليل من TradingView
def analyze(symbol="BTCUSDT"):
    handler = TA_Handler(
        symbol=symbol,
        screener="crypto",
        exchange="BINANCE",
        interval=Interval.INTERVAL_5_MINUTES
    )

    analysis = handler.get_analysis()

    summary = analysis.summary
    indicators = analysis.indicators

    signal = summary["RECOMMENDATION"]
    rsi = indicators["RSI"]

    return f"""
📊 {symbol}
━━━━━━━━━━━
🔹 Signal: {signal}
🔹 RSI: {rsi:.2f}
🔹 BUY: {summary['BUY']}
🔹 SELL: {summary['SELL']}
🔹 NEUTRAL: {summary['NEUTRAL']}
"""

# أوامر البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔥 بوت TradingView جاهز!\nاكتب /btc")

async def btc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = analyze("BTCUSDT")
    await update.message.reply_text(result)

async def eth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = analyze("ETHUSDT")
    await update.message.reply_text(result)

# تشغيل البوت
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("btc", btc))
app.add_handler(CommandHandler("eth", eth))

print("Bot Running...")
app.run_polling()
