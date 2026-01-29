import requests
import os
from telegram.ext import ApplicationBuilder, CommandHandler
from datetime import datetime, timedelta

TOKEN = os.getenv("BOT_TOKEN")

BINANCE_P2P = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"


def get_p2p_price(trade_type):
    payload = {
        "asset": "USDT",
        "fiat": "VND",
        "page": 1,
        "rows": 1,
        "tradeType": trade_type
    }

    r = requests.post(BINANCE_P2P, json=payload, timeout=10)
    data = r.json()

    return float(data["data"][0]["adv"]["price"])


def get_usdt_p2p():
    # Chuẩn VN:
    buy_price = get_p2p_price("BUY")     # anh mua USDT
    sell_price = get_p2p_price("SELL")   # anh bán USDT

    avg = int((buy_price + sell_price) / 2)

    return int(buy_price), int(sell_price), avg


async def usdt(update, context):
    try:
        buy, sell, avg = get_usdt_p2p()
        now = (datetime.utcnow() + timedelta(hours=7)).strftime("%H:%M %d/%m")

        text = (
            f"🕐 {now}\n"
            f"📈 Mua USDT: {buy:,} VND\n"
            f"📉 Bán USDT: {sell:,} VND\n"
            f"⚖ Trung bình: {avg:,} VND\n"
            f"📊 Binance P2P"
        )

        await update.message.reply_text(text)

    except Exception as e:
        print("ERROR:", e)
        await update.message.reply_text("⚠ Không lấy được giá, thử lại sau.")


app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("usdt", usdt))

print("Bot running...")
app.run_polling()
