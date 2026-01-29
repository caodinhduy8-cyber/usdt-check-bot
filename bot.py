import requests
from bs4 import BeautifulSoup
from telegram.ext import ApplicationBuilder, CommandHandler
from datetime import datetime
import pytz
import os

TOKEN = os.getenv("BOT_TOKEN") or "DAN_TOKEN_BOT_CUA_ANH_VAO_DAY"

URL = "https://moneyexchange247.com"

def get_usdt_avg():
    r = requests.get(URL, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    prices = soup.find_all("span", class_="price")

    usdt_prices = []
    for p in prices:
        text = p.text.replace(",", "").replace(" VND", "").strip()
        if text.isdigit():
            usdt_prices.append(int(text))

    # USDT thường là dòng thứ 2 (mua) và thứ 3 (bán)
    buy = usdt_prices[1]
    sell = usdt_prices[2]

    avg = int((buy + sell) / 2)

    return buy, sell, avg


async def usdt(update, context):
    try:
        buy, sell, avg = get_usdt_avg()

        vn_time = datetime.now(pytz.timezone("Asia/Ho_Chi_Minh")).strftime("%H:%M %d/%m")

        msg = (
            f"🕐 {vn_time}\n"
            f"💵 Mua: {buy:,} VND\n"
            f"💰 Bán: {sell:,} VND\n"
            f"📊 Trung bình: {avg:,} VND\n"
            f"(Nguồn: MoneyExchange247)"
        )

        await update.message.reply_text(msg)

    except Exception as e:
        await update.message.reply_text("⚠ Không lấy được giá USDT, thử lại sau.")


app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("usdt", usdt))

print("Bot USDT đang chạy...")
app.run_polling()
