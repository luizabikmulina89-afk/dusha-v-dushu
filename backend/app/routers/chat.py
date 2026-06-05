from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.database import get_db
from app import models
from app.schemas import MessageSend

router = APIRouter(prefix="/chat", tags=["chat"])

CHAT_EXPIRY_DAYS = 10


@router.get("/{match_id}")
def get_messages(match_id: int, telegram_id: int, db: Session = Depends(get_db)):
    me = db.query(models.User).filter(models.User.telegram_id == telegram_id).first()
    if not me:
        raise HTTPException(404, "Пользователь не найден")

    match = db.query(models.Match).filter(models.Match.id == match_id).first()
    if not match:
        raise HTTPException(404, "Совпадение не найдено")

    if match.user1_id != me.id and match.user2_id != me.id:
        raise HTTPException(403, "Нет доступа")

    messages = (
        db.query(models.Message)
        .filter(models.Message.match_id == match_id)
        .order_by(models.Message.created_at)
        .all()
    )

    # Отмечаем входящие как прочитанные
    db.query(models.Message).filter(
        models.Message.match_id == match_id,
        models.Message.from_user_id != me.id,
        models.Message.is_read == False,
    ).update({"is_read": True})
    db.commit()

    return {
        "messages": [
            {
                "id": m.id,
                "from_user_id": m.from_user_id,
                "text": m.text,
                "is_mine": m.from_user_id == me.id,
                "created_at": m.created_at.isoformat(),
                "is_read": m.is_read,
            }
            for m in messages
        ],
        "match_expires_at": match.expires_at.isoformat() if match.expires_at else None,
    }


@router.post("/{match_id}/send")
def send_message(
    match_id: int,
    telegram_id: int,
    body: MessageSend,
    db: Session = Depends(get_db),
):
    me = db.query(models.User).filter(models.User.telegram_id == telegram_id).first()
    if not me:
        raise HTTPException(404, "Пользователь не найден")

    match = db.query(models.Match).filter(models.Match.id == match_id).first()
    if not match:
        raise HTTPException(404, "Совпадение не найдено")

    if match.user1_id != me.id and match.user2_id != me.id:
        raise HTTPException(403, "Нет доступа")

    msg = models.Message(
        match_id=match_id,
        from_user_id=me.id,
        text=body.text,
        media_type="text",
    )
    db.add(msg)

    # Сброс антигостинг-таймера
    match.last_message_at = datetime.utcnow()
    match.expires_at = datetime.utcnow() + timedelta(days=CHAT_EXPIRY_DAYS)
    db.commit()
    db.refresh(msg)

    # Уведомление получателю
    partner_id = match.user2_id if match.user1_id == me.id else match.user1_id
    partner = db.query(models.User).filter(models.User.id == partner_id).first()
    if partner:
        try:
            from app.notifications import send_notification
            send_notification(
                partner.telegram_id,
                f"💬 Новое сообщение от {me.pseudonym}:\n{body.text[:100]}"
            )
        except Exception:
            pass

    return {"ok": True, "message_id": msg.id}
