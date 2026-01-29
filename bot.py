import requests
from telegram.ext import ApplicationBuilder, CommandHandler
from datetime import datetime
import os

TOKEN = os.getenv("BOT_TOKEN")

def get_usdt_vnd():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=USDTVND"
    return int(float(requests.get(url).json()["price"]))

async def check(update, context):
    price = get_usdt_vnd()
    now = datetime.now().strftime("%H:%M %d/%m")
    await update.message.reply_text(f"💰 USDT: {price:,} VND\n🕐 {now}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("check", check))
app.run_polling()
