from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "PUT_YOUR_BOT_TOKEN_HERE"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 البوت يعمل بنجاح!")

async def analysis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📊 تحليل السوق قيد التطوير...")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("analysis", analysis))

app.run_polling()
