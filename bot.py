import requests
from telegram.ext import ApplicationBuilder, CommandHandler
from datetime import datetime
import os

TOKEN = os.getenv("BOT_TOKEN") or "DAN_TOKEN_BOT_CUA_ANH_VAO_DAY"

def get_usdt_vnd():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=USDTVND"
    return int(float(requests.get(url).json()["price"]))

async def usdt(update, context):
    price = get_usdt_vnd()
    now = datetime.now().strftime("%H:%M %d/%m")
    await update.message.reply_text(
        f"💰 USDT: {price:,} VND\n🕐 {now}"
    )

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("usdt", usdt))

print("Bot USDT đang chạy...")
app.run_polling()
