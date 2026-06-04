import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

load_dotenv("../backend/.env")

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
MINI_APP_URL = os.getenv("MINI_APP_URL", "https://your-domain.com")

logging.basicConfig(level=logging.INFO)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name or "друг"

    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton(
            text="✨ Открыть Душа в душу",
            web_app=WebAppInfo(url=MINI_APP_URL)
        )
    ]])

    await update.message.reply_text(
        f"Привет, {name}! 🌟\n\n"
        "«Душа в душу» — это не просто знакомства.\n"
        "Здесь тебя ждут люди, с которыми ты совместим(а) "
        "по нумерологии, астрологии, Human Design и ещё 6 системам.\n\n"
        "Нажми кнопку ниже, чтобы начать:",
        reply_markup=keyboard
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔮 Команды:\n"
        "/start — открыть приложение\n"
        "/help — эта справка\n\n"
        "По всем вопросам: @DushaVDushuHelp"
    )


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    print("Бот запущен.")
    app.run_polling()


if __name__ == "__main__":
    main()
