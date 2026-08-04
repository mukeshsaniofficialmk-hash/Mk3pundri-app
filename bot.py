import json
import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_FATHER_TOKEN")
# आपका exact GitHub Pages URL
WEB_APP_URL = "https://mukeshsaniofficialmk-hash.github.io/Mk3pundri-app/"
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID", "YOUR_PERSONAL_TELEGRAM_CHAT_ID")

def get_inchat_ad():
    try:
        res = requests.get("https://api.adexium.com/v1/get-ad", headers={"Authorization": "Bearer YOUR_KEY"})
        if res.status_code == 200:
            return res.json().get("ad_text")
    except Exception:
        return None
    return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ad = get_inchat_ad()
    msg = "👋 *Mk3 Pundri Watch & Earn Bot* में आपका स्वागत है!\n\n" \
          "🎮 गेम्स खेलें, टास्क पूरा करें और ऐड्स देखकर Google Pay में पैसे कमाएं।\n" \
          "💰 *दर:* 1000 Coins = ₹10\n\n"
    if ad:
        msg += f"-------------------\n📢 प्रायोजित (Sponsored): {ad}"

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 Open App & Earn", web_app=WebAppInfo(url=WEB_APP_URL))]
    ])
    await update.message.reply_text(msg, reply_markup=keyboard, parse_mode="Markdown")

async def handle_webapp_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = json.loads(update.message.web_app_data.data)
    if data.get("action") == "withdraw":
        user = update.message.from_user
        upi = data.get("upi_id")
        coins = data.get("coins")
        inr_amount = data.get("amount_inr")

        admin_msg = (
            f"🔔 *नई Payout Request (Google Pay / UPI)!*\n\n"
            f"👤 *यूज़र:* {user.first_name} (@{user.username})\n"
            f"🆔 *User ID:* `{user.id}`\n"
            f"📍 *UPI ID:* `{upi}`\n"
            f"🪙 *Coins Used:* {coins}\n"
            f"💵 *भुगतान राशि:* ₹{inr_amount}"
        )
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_msg, parse_mode="Markdown")
        await update.message.reply_text(f"✅ आपकी ₹{inr_amount} की विथड्रॉल रिक्वेस्ट एडमिन को भेज दी गई है।")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_webapp_data))
    app.run_polling()
