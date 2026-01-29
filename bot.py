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

    rows = soup.select("div.rate-row")

    buy = None
    sell = None

    for row in rows:
        name = row.text.lower()
        price = row.find("span", class_="price")

        if not price:
            continue

        value = int(price.text.replace(",", "").replace(" VND", ""))

        if "usdt" in name and buy is None:
            buy = value
        elif "usdt" in name and buy is not None:
            sell = value
            break

    if buy is None or sell is None:
        raise Exception("Không lấy được giá")

    avg = int((buy + sell) / 2)
    return buy, sell, avg


async def usdt(update, context):
    try:
        buy, sell, avg = get_usdt_avg()

        vn_time = datetime.now(pytz.timezone("Asia/Ho_Chi_Minh")).strftime("%H:%M %d/%m")

        text = (
            f"🕐 {vn_time}\n"
            f"💵 Mua: {buy:,} VND\n"
            f"💰 Bán: {sell:,} VND\n"
            f"📊 Trung bình: {avg:,} VND\n"
            f"(Nguồn: MoneyExchange247)"
        )

        await update.message.reply_text(text)

    except:
        await update.message.reply_text("⚠ Không lấy được giá USDT, thử lại sau.")


app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("usdt", usdt))

print("Bot đang chạy...")
app.run_polling()
