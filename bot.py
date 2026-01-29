import requests
from telegram.ext import ApplicationBuilder, CommandHandler
from datetime import datetime, timedelta
import os
from bs4 import BeautifulSoup

TOKEN = os.getenv("BOT_TOKEN") or "DAN_TOKEN_BOT_CUA_ANH_VAO_DAY"
URL = "https://moneyexchange247.com"

def get_usdt_prices():
    html = requests.get(URL, timeout=10).text
    soup = BeautifulSoup(html, "html.parser")

    buy_block = soup.find("div", string="USDT").find_parent("div")
    buy_price = int(buy_block.find("span").text.replace(",", "").replace(" VND", ""))

    sell_section = soup.find("div", string="Bạn muốn BÁN")
    sell_block = sell_section.find_next("div", string="USDT").find_parent("div")
    sell_price = int(sell_block.find("span").text.replace(",", "").replace(" VND", ""))

    return buy_price, sell_price


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
