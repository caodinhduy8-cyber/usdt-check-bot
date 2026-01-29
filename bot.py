import requests
from telegram.ext import ApplicationBuilder, CommandHandler
from datetime import datetime, timedelta
import os

TOKEN = os.getenv("BOT_TOKEN") or "DAN_TOKEN_BOT_CUA_ANH_VAO_DAY"

API_URL = "https://moneyexchange247.com/api/rate"

def get_usdt_prices():
    data = requests.get(API_URL, timeout=10).json()

    buy = int(data["USDT"]["buy"])
    sell = int(data["USDT"]["sell"])

    return buy, sell


async def usdt(update, context):
    try:
        buy, sell = get_usdt_prices()
        avg = int((buy + sell) / 2)

        now = (datetime.utcnow() + timedelta(hours=7)).strftime("%H:%M %d/%m")

        await update.message.reply_text(
            f"🕐 {now}\n"
            f"💵 Mua: {buy:,} VND\n"
            f"💰 Bán: {sell:,} VND\n"
            f"📊 Trung bình: {avg:,} VND\n"
            f"(Nguồn: MoneyExchange247)"
        )

    except Exception as e:
        print("ERROR:", e)
        await update.message.reply_text("⚠ Không lấy được giá USDT, thử lại sau.")


app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("usdt", usdt))

print("Bot đang chạy...")
app.run_polling()
