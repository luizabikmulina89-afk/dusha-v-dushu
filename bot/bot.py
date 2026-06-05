import os
import logging
import httpx
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import (
    Application, CommandHandler, PreCheckoutQueryHandler,
    MessageHandler, filters, ContextTypes,
)

load_dotenv("../backend/.env")

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
MINI_APP_URL = os.getenv("MINI_APP_URL", "https://your-domain.com")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

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


async def pre_checkout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Telegram требует ответить на pre_checkout_query в течение 10 секунд."""
    await update.pre_checkout_query.answer(ok=True)


async def successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Вызывается когда пользователь успешно оплатил Stars."""
    telegram_id = update.effective_user.id
    try:
        httpx.post(
            f"{BACKEND_URL}/payments/activate/{telegram_id}",
            timeout=5.0,
        )
    except Exception as e:
        logging.error(f"Failed to activate premium for {telegram_id}: {e}")

    await update.message.reply_text(
        "✨ Premium активирован на 30 дней!\n\n"
        "Теперь тебе доступны:\n"
        "• Безлимитная лента кандидатов\n"
        "• Суперлайки каждый день\n"
        "• Полная разбивка по 9 системам\n\n"
        "Открой приложение и найди своего человека! 💫"
    )


def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(PreCheckoutQueryHandler(pre_checkout))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment))
    print("Бот запущен.")
    app.run_polling()


if __name__ == "__main__":
    main()
