import requests
from telegram.ext import ApplicationBuilder, CommandHandler
from datetime import datetime
import os

TOKEN = os.getenv("BOT_TOKEN") or "DAN_TOKEN_BOT_CUA_ANH_VAO_DAY"

P2P_URL = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"

def get_usdt_vnd():
    payload = {
        "asset": "USDT",
        "fiat": "VND",
        "tradeType": "BUY",
        "page": 1,
        "rows": 1
    }

    try:
        r = requests.post(P2P_URL, json=payload, timeout=10).json()
        return int(float(r["data"][0]["adv"]["price"]))
    except Exception:
        return None

async def usdt(update, context):
    now = datetime.now().strftime("%H:%M %d/%m")

    price = get_usdt_vnd()
    if not price:
        await update.message.reply_text("⚠️ Không lấy được giá USDT, thử lại sau.")
        return

    await update.message.reply_text(
        f"🕐 {now}\n"
        f"💰 USDT: {price:,} VND\n"
        f"(Nguồn: Binance P2P)"
    )

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("usdt", usdt))

print("Bot USDT đang chạy...")
app.run_polling()
