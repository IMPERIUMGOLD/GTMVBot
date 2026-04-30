from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

import os
TOKEN = os.getenv("8677648639:AAGgs8w5aijNTf2E5cEqdl9G2oLhQakIMGs")

ADMIN_LINK = "https://t.me/theonlymarsadmin_Lucy"

SG_LINK = "https://portal.fortuneprime.com/getview?view=register&token=0n6r0B"
GLOBAL_LINK = "https://www.vantagemarkets.io/en/open-live-account/?affid=NzI2MTI3NQ=="


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

    if query.data == "menu":
        await show_menu(query)

    # ===== SGCN（第二张图）=====
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

            f"Step 1:\n"
            f"Click [HERE]({SG_LINK}) to register account with our broker FPG (Fortune Prime Global).\n\n"

            f"Step 2:\n"
            f"Account type select Standard Acc and deposit min. 150USD.\n\n"

            f"Step 3:\n"
            f"Make sure complete KYC Account Verification.\n\n"

            f"Step 4:\n"
            f"Provide below details:\n\n"

            f"```\n"
            f"Full Name :\n"
            f"Email :\n"
            f"Trading Account Number (ID) :\n"
            f"```",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    # ===== GLOBAL（第一张图）=====
    elif query.data == "global":
        keyboard = [
            [InlineKeyboardButton("✅ I’ve Completed All Steps", url=ADMIN_LINK)],
            [InlineKeyboardButton("📩 Need More Help", url=ADMIN_LINK)],
            [InlineKeyboardButton("🔁 Change IB", callback_data="ib")],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="menu")]
        ]

        await query.edit_message_text(
            f"HOW TO STEP CLOSE WITH MARS???\n\n"
            f"Follow the step as below ⬇️\n\n"

            f"1. Click [HERE]({GLOBAL_LINK}) to register your account.\n"
            f"2. KYC Account Verification\n"
            f"3. Account type only STP Standard.\n"
            f"4. Deposit 100USD & Screenshot to us.\n"
            f"5. Provide below details\n\n"

            f"```\n"
            f"Full Name :\n"
            f"Email :\n"
            f"Vantage Account Number (UID) :\n"
            f"```\n\n"

            f"* Referral by : GTMars *\n\n"
            f"Once done, be patient wait for account checking.\n"
            f"Thank you 🏆",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    # ===== IB =====
    elif query.data == "ib":
        keyboard = [
            [InlineKeyboardButton("📩 Contact Admin", url=ADMIN_LINK)],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="menu")]
        ]

        await query.edit_message_text(
            "🔁 Change IB Request\n\n"
            "Kindly copy the format below and send it to our admin 👇\n\n"
            "-------------------------\n"
            "Full Name:\n"
            "Email:\n"
            "Client ID:\n"
            "-------------------------\n\n"
            "We will process your request as soon as possible 🚀",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

print("Bot is running...")

app.run_polling()

