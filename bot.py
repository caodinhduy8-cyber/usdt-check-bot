import requests
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update
from datetime import datetime, timedelta

TOKEN = "YOUR_BOT_TOKEN"

# ID Telegram của bạn (khóa quyền)
OWNER_ID = 8388605825

BINANCE_P2P_URL = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"

def get_p2p_price(trade_type):
    payload = {
        "page": 1,
        "rows": 1,
        "payTypes": [],
        "asset": "USDT",
        "tradeType": trade_type,
        "fiat": "VND"
    }
    r = requests.post(BINANCE_P2P_URL, json=payload, timeout=10)
    data = r.json()["data"][0]
    return float(data["adv"]["price"])

async def usdt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        buy = get_p2p_price("BUY")   # người bán USDT cho mình → giá mua
        sell = get_p2p_price("SELL") # mình bán USDT → giá bán
        avg = (buy + sell) / 2

        now = datetime.utcnow() + timedelta(hours=7)

        msg = (
            f"🕒 {now.strftime('%H:%M %d/%m')}\n"
            f"💵 Mua: {int(buy):,} VND\n"
            f"💸 Bán: {int(sell):,} VND\n"
            f"📊 Trung bình: {int(avg):,} VND\n"
            f"(Nguồn: Binance P2P)"
        )

        await update.message.reply_text(msg)

    except Exception:
        await update.message.reply_text("⚠ Không lấy được giá USDT, thử lại sau.")

# Chặn người khác thêm bot vào nhóm
async def block_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != OWNER_ID:
        await update.message.reply_text("⛔ Bạn không có quyền sử dụng bot này.")
        return

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("usdt", usdt))
    app.add_handler(CommandHandler("start", block_add))

    print("Bot đang chạy...")
    app.run_polling()

if __name__ == "__main__":
    main()
