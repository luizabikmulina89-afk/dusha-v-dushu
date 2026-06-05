import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.database import get_db
from app import models
from app.config import settings

router = APIRouter(prefix="/payments", tags=["payments"])

PREMIUM_DAYS = 30
PREMIUM_STARS_PRICE = 99


@router.post("/create-invoice/{telegram_id}")
def create_invoice(telegram_id: int, db: Session = Depends(get_db)):
    """Создаёт ссылку на инвойс Telegram Stars и возвращает её фронтенду."""
    user = db.query(models.User).filter(models.User.telegram_id == telegram_id).first()
    if not user:
        raise HTTPException(404, "Пользователь не найден")

    if not settings.telegram_bot_token:
        raise HTTPException(503, "Платежи не настроены")

    url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/createInvoiceLink"
    try:
        res = httpx.post(
            url,
            json={
                "title": "Premium — Душа в душу",
                "description": (
                    "30 дней: безлимитная лента, суперлайки каждый день, "
                    "полная разбивка совместимости"
                ),
                "payload": f"premium_{telegram_id}",
                "currency": "XTR",
                "prices": [{"label": "Premium 30 дней", "amount": PREMIUM_STARS_PRICE}],
            },
            timeout=10.0,
        )
        data = res.json()
        if not data.get("ok"):
            raise HTTPException(500, f"Telegram API error: {data.get('description')}")
        return {"invoice_link": data["result"]}
    except httpx.TimeoutException:
        raise HTTPException(503, "Сервис Telegram недоступен")


@router.post("/activate/{telegram_id}")
def activate_premium(telegram_id: int, db: Session = Depends(get_db)):
    """Активирует Premium. Вызывается ботом после успешной оплаты Stars."""
    user = db.query(models.User).filter(models.User.telegram_id == telegram_id).first()
    if not user:
        raise HTTPException(404, "Пользователь не найден")

    user.is_premium = True
    user.premium_expires = datetime.utcnow() + timedelta(days=PREMIUM_DAYS)
    db.commit()
    return {"ok": True, "premium_expires": user.premium_expires.isoformat()}
