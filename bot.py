import requests
from telegram.ext import ApplicationBuilder, CommandHandler
from datetime import datetime, timedelta
import os

TOKEN = os.getenv("BOT_TOKEN") or "DAN_TOKEN_BOT_CUA_ANH_VAO_DAY"

def get_p2p_price(trade_type):
    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    payload = {
        "asset": "USDT",
        "fiat": "VND",
        "page": 1,
        "rows": 1,
        "tradeType": trade_type
    }
    r = requests.post(url, json=payload, timeout=10).json()
    return float(r["data"][0]["adv"]["price"])

def get_usdt_p2p():
    # ĐẢO CHIỀU CHO ĐÚNG THỊ TRƯỜNG
    sell_price = get_p2p_price("BUY")    # người bán rẻ nhất
    buy_price = get_p2p_price("SELL")    # người mua trả cao nhất

    avg = int((buy_price + sell_price) / 2)
    return int(buy_price), int(sell_price), avg

async def usdt(update, context):
    try:
        buy, sell, avg = get_usdt_p2p()
        now = (datetime.utcnow() + timedelta(hours=7)).strftime("%H:%M %d/%m")

        await update.message.reply_text(
            f"🕐 {now}\n"
            f"📈 Mua: {buy:,} VND\n"
            f"📉 Bán: {sell:,} VND\n"
            f"⚖ Trung bình: {avg:,} VND\n"
            f"(Nguồn: Binance P2P)"
        )
    except Exception as e:
        print(e)
        await update.message.reply_text("⚠ Lỗi lấy giá, thử lại.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("usdt", usdt))

print("Bot P2P running...")
app.run_polling()
