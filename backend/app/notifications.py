import httpx
from app.config import settings


def send_notification(telegram_id: int, text: str) -> None:
    """Отправляет уведомление через Telegram Bot API. Fire-and-forget."""
    if not settings.telegram_bot_token:
        return
    url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"
    try:
        httpx.post(
            url,
            json={"chat_id": telegram_id, "text": text},
            timeout=3.0,
        )
    except Exception:
        pass
