import requests
from telegram.ext import ApplicationBuilder, CommandHandler
from datetime import datetime
import os

TOKEN = os.getenv("BOT_TOKEN") or "DAN_TOKEN_BOT_CUA_ANH_VAO_DAY"


def get_usdt_vnd():
    try:
        url = "https://api.binance.com/api/v3/ticker/price?symbol=USDTBUSD"
        res = requests.get(url, timeout=5).json()
        usdt_usd = float(res["price"])

        # tỷ giá USD/VND ước lượng (ổn định hơn)
        usd_vnd = 26500  

        return int(usdt_usd * usd_vnd)

    except Exception:
        return None


async def usdt(update, context):
    price = get_usdt_vnd()
    now = datetime.now().strftime("%H:%M %d/%m")

    if price is None:
        await update.message.reply_text("⚠️ Không lấy được giá USDT, thử lại sau.")
        return

    await update.message.reply_text(
        f"💰 USDT ≈ {price:,} VND\n🕐 {now}"
    )


app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("usdt", usdt))

print("Bot USDT đang chạy...")
app.run_polling()
