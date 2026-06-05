import os
import logging
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database import engine, Base
from app import models  # noqa: F401
from app.routers import users, feed, likes, chat, payments
from app.config import settings

log = logging.getLogger(__name__)

# Путь к папке frontend (на 3 уровня выше backend/app/main.py)
_frontend_dir = Path(__file__).parent.parent.parent / "frontend"
FRONTEND_DIR = Path(os.getenv("FRONTEND_PATH", str(_frontend_dir)))

# Глобальный объект Telegram Bot (инициализируется при старте, если задан токен)
_bot = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _bot

    Base.metadata.create_all(bind=engine)

    if settings.telegram_bot_token:
        try:
            from telegram import Bot
            _bot = Bot(token=settings.telegram_bot_token)
            webhook_url = f"{settings.backend_url.rstrip('/')}/webhook"
            await _bot.set_webhook(url=webhook_url)
            log.info(f"Webhook установлен: {webhook_url}")
        except Exception as e:
            log.warning(f"Не удалось установить webhook: {e}")

    yield

    if _bot:
        try:
            await _bot.delete_webhook()
        except Exception:
            pass


app = FastAPI(title="Душа в душу API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(feed.router)
app.include_router(likes.router)
app.include_router(chat.router)
app.include_router(payments.router)


@app.get("/")
def root():
    return {"status": "ok", "app": "Душа в душу"}


@app.post("/webhook")
async def telegram_webhook(request: Request):
    """Принимает обновления от Telegram (webhook режим для продакшена)."""
    if not _bot:
        return {"ok": False, "reason": "bot not configured"}

    import httpx as _httpx
    data = await request.json()

    # Подтверждение pre_checkout (обязательно в течение 10 сек)
    if "pre_checkout_query" in data:
        pq = data["pre_checkout_query"]
        try:
            await _bot.answer_pre_checkout_query(
                pre_checkout_query_id=pq["id"], ok=True
            )
        except Exception as e:
            log.error(f"pre_checkout error: {e}")
        return {"ok": True}

    msg = data.get("message", {})

    # Успешная оплата Stars → активируем Premium
    if "successful_payment" in msg:
        telegram_id = msg["from"]["id"]
        try:
            _httpx.post(
                f"http://localhost:{os.getenv('PORT', '8000')}/payments/activate/{telegram_id}",
                timeout=5.0,
            )
        except Exception as e:
            log.error(f"activate premium error: {e}")
        try:
            await _bot.send_message(
                chat_id=telegram_id,
                text=(
                    "✨ Premium активирован на 30 дней!\n\n"
                    "Теперь тебе доступны:\n"
                    "• Безлимитная лента кандидатов\n"
                    "• Суперлайки каждый день\n"
                    "• Полная разбивка по 9 системам\n\n"
                    "Открой приложение и найди своего человека! 💫"
                ),
            )
        except Exception as e:
            log.error(f"send premium message error: {e}")
        return {"ok": True}

    # /start — отправляем кнопку Mini App
    text = msg.get("text", "")
    if text.startswith("/start"):
        from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
        chat_id = msg["chat"]["id"]
        name = msg.get("from", {}).get("first_name", "друг")
        keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton(
                text="✨ Открыть Душа в душу",
                web_app=WebAppInfo(url=settings.mini_app_url),
            )
        ]])
        try:
            await _bot.send_message(
                chat_id=chat_id,
                text=(
                    f"Привет, {name}! 🌟\n\n"
                    "«Душа в душу» — это не просто знакомства.\n"
                    "Здесь тебя ждут люди, с которыми ты совместим(а) "
                    "по нумерологии, астрологии, Human Design и ещё 6 системам.\n\n"
                    "Нажми кнопку ниже, чтобы начать:"
                ),
                reply_markup=keyboard,
            )
        except Exception as e:
            log.error(f"send start message error: {e}")

    return {"ok": True}


# Раздача фронтенда — после всех API-роутов
if FRONTEND_DIR.exists():
    app.mount("/app", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
