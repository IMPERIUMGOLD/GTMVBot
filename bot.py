import os
import threading
from datetime import datetime
from zoneinfo import ZoneInfo
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

ADMIN_LINK = "https://t.me/theonlymarsadmin_Lucy"
SG_LINK = "https://portal.fortuneprime.com/getview?view=register&token=0n6r0B"
GLOBAL_LINK = "https://www.vantagemarkets.io/en/open-live-account/?affid=NzI2MTI3NQ=="

PROMO_TITLE = "🎉 EARLY BIRD PROMO 🔥"
PROMO_PRICE = "70USD"
NORMAL_PRICE = "150USD"

PROMO_START = datetime(2026, 5, 14, 0, 0, tzinfo=ZoneInfo("Asia/Singapore"))
PROMO_END = datetime(2026, 5, 31, 23, 59, tzinfo=ZoneInfo("Asia/Singapore"))


def promo_active():
    now = datetime.now(ZoneInfo("Asia/Singapore"))
    return PROMO_START <= now <= PROMO_END


def get_promo_text():
    if promo_active():
        return (
            f"{PROMO_TITLE}\n\n"
            f"<b>Promo Period : 14/05/2026 - 31/05/2026</b>\n\n"
        )
    return ""


def get_deposit_amount():
    return PROMO_PRICE if promo_active() else NORMAL_PRICE


web_app = Flask(__name__)


@web_app.route("/")
def home():
    return "Bot is running."


def run_web():
    port = int(os.getenv("PORT", 10000))
    web_app.run(host="0.0.0.0", port=port)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🇸🇬 🇨🇳 Singapore & China Member", callback_data="sgcn")],
        [InlineKeyboardButton("🌍 All Countries (Excluding SG & CN)", callback_data="global")]
    ]

    await update.message.reply_text(
        "🌍 Please select your region to continue, your country👇\n\n"
        "✨ This helps us provide the most suitable service for you.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def show_menu(query):
    keyboard = [
        [InlineKeyboardButton("🇸🇬 🇨🇳 Singapore & China Member", callback_data="sgcn")],
        [InlineKeyboardButton("🌍 All Countries (Excluding SG & CN)", callback_data="global")]
    ]

    await query.edit_message_text(
        "🌍 Please select your region to continue, your country👇\n\n"
        "✨ This helps us provide the most suitable service for you.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    deposit_amount = get_deposit_amount()
    promo_text = get_promo_text()

    if query.data == "menu":
        await show_menu(query)

    elif query.data == "sgcn":
        keyboard = [
            [InlineKeyboardButton("✅ I’ve Completed All Steps", url=ADMIN_LINK)],
            [InlineKeyboardButton("📩 Need More Help", url=ADMIN_LINK)],
            [InlineKeyboardButton("🔁 Change IB", callback_data="ib")],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="menu")]
        ]

        await query.edit_message_text(
            f"Hi There 👋\n\n"
            f"🇸🇬 🇨🇳 How to join Fighter GTMV? Very simple!\n\n"
            f"{promo_text}"
            f"Step 1:\n"
            f'Click <a href="{SG_LINK}"><b>HERE</b></a> to register account with our broker FPG (Fortune Prime Global).\n\n'
            f"Step 2:\n"
            f"Account type select Standard Acc and deposit min. {deposit_amount}.\n\n"
            f"Step 3:\n"
            f"Make sure complete KYC Account Verification.\n\n"
            f"Step 4:\n"
            f"Provide below details:\n\n"
            f"<pre>Full Name :\nEmail :\nTrading Account Number (ID) :</pre>",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML",
            disable_web_page_preview=True
        )

    elif query.data == "global":
        keyboard = [
            [InlineKeyboardButton("✅ I’ve Completed All Steps", url=ADMIN_LINK)],
            [InlineKeyboardButton("📩 Need More Help", url=ADMIN_LINK)],
            [InlineKeyboardButton("🔁 Change IB", callback_data="ib")],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="menu")]
        ]

        await query.edit_message_text(
            f"HOW TO STEP CLOSE WITH MARS???\n\n"
            f"{promo_text}"
            f"Follow the step as below ⬇️\n\n"
            f'1. Click <a href="{GLOBAL_LINK}"><b>HERE</b></a> to register your account.\n'
            f"2. KYC Account Verification\n"
            f"3. Account type only STP Standard.\n"
            f"4. Deposit {deposit_amount} & Screenshot to us.\n"
            f"5. Provide below details\n\n"
            f"<pre>Full Name :\nEmail :\nVantage Account Number (UID) :</pre>\n\n"
            f"<b><i>Referral by : GTMars</i></b>\n\n"
            f"Once done, be patient wait for account checking.\n"
            f"Thank you 🏆",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML",
            disable_web_page_preview=True
        )

    elif query.data == "ib":
        keyboard = [
            [InlineKeyboardButton("📩 Contact Admin", url=ADMIN_LINK)],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="menu")]
        ]

        await query.edit_message_text(
            "🔁 Change IB Request\n\n"
            "Kindly copy the format below and send it to our admin 👇\n\n"
            "<pre>Full Name:\nEmail:\nClient ID:</pre>\n\n"
            "We will process your request as soon as possible 🚀",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML"
        )


if not TOKEN:
    raise ValueError("TOKEN is missing. Please set TOKEN in Render Environment Variables.")

threading.Thread(target=run_web, daemon=True).start()

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

print("Bot is running...")
app.run_polling()
