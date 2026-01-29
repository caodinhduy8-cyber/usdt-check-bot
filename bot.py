import requests
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from telegram import Update
from datetime import datetime, timedelta

TOKEN = "YOUR_BOT_TOKEN"
OWNER_ID = 8388605825

BINANCE_URL = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"

def get_price(type_):
    payload = {
        "page": 1,
        "rows": 1,
        "asset": "USDT",
        "tradeType": type_,
        "fiat": "VND",
        "payTypes": []
    }
    r = requests.post(BINANCE_URL, json=payload, timeout=10)
    return float(r.json()["data"][0]["adv"]["price"])

async def usdt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        buy = get_price("BUY")
        sell = get_price("SELL")
        avg = (buy + sell) / 2

        now = datetime.utcnow() + timedelta(hours=7)

        text = (
            f"🕒 {now.strftime('%H:%M %d/%m')}\n"
            f"💵 Mua: {int(buy):,} VND\n"
            f"💸 Bán: {int(sell):,} VND\n"
            f"📊 Trung bình: {int(avg):,} VND\n"
            f"(Binance P2P)"
        )

        await update.message.reply_text(text)

    except Exception as e:
        await update.message.reply_text("⚠ Lỗi lấy giá, thử lại sau.")

# 🔐 Chặn người khác add bot
async def on_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        if member.id == context.bot.id:
            adder = update.effective_user.id
            if adder != OWNER_ID:
                await context.bot.leave_chat(update.effective_chat.id)

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("usdt", usdt))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, on_new_member))

    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
