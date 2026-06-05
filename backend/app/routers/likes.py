from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.database import get_db
from app import models
from app.calculations.compatibility import calculate_compatibility

router = APIRouter(prefix="/likes", tags=["likes"])

CHAT_EXPIRY_DAYS = 10


@router.post("/{telegram_id}/like/{target_user_id}")
def send_like(
    telegram_id: int,
    target_user_id: int,
    is_super: bool = False,
    db: Session = Depends(get_db)
):
    me = db.query(models.User).filter(models.User.telegram_id == telegram_id).first()
    if not me:
        raise HTTPException(404, "Пользователь не найден")

    target = db.query(models.User).filter(models.User.id == target_user_id).first()
    if not target:
        raise HTTPException(404, "Кандидат не найден")

    existing = db.query(models.Like).filter(
        models.Like.from_user_id == me.id,
        models.Like.to_user_id == target_user_id
    ).first()
    if existing:
        return {"ok": True, "already_liked": True, "matched": False}

    like = models.Like(from_user_id=me.id, to_user_id=target_user_id, is_super=is_super)
    db.add(like)

    mutual = db.query(models.Like).filter(
        models.Like.from_user_id == target_user_id,
        models.Like.to_user_id == me.id
    ).first()

    matched = False
    match_id = None

    if mutual:
        p1 = _build_compat_profile_from_user(me)
        p2 = _build_compat_profile_from_user(target)
        compat = calculate_compatibility(p1, p2)

        match = models.Match(
            user1_id=me.id,
            user2_id=target.id,
            compatibility_score=compat.get("total", 0),
            compatibility_breakdown=compat.get("breakdown", {}),
            systems_used=compat.get("systems_used", 0),
            expires_at=datetime.utcnow() + timedelta(days=CHAT_EXPIRY_DAYS),
        )
        db.add(match)
        db.flush()
        matched = True
        match_id = match.id

    db.commit()

    # Уведомляем обоих при матче
    if matched:
        try:
            from app.notifications import send_notification
            send_notification(
                me.telegram_id,
                f"💫 Космическое совпадение с {target.pseudonym}!\n"
                f"Совместимость: {round(match.compatibility_score)}%\n"
                "Откройте приложение и начните общение!"
            )
            send_notification(
                target.telegram_id,
                f"💫 Космическое совпадение с {me.pseudonym}!\n"
                f"Совместимость: {round(match.compatibility_score)}%\n"
                "Откройте приложение и начните общение!"
            )
        except Exception:
            pass

    return {
        "ok": True,
        "matched": matched,
        "match_id": match_id,
        "is_super": is_super,
    }


@router.get("/{telegram_id}/matches")
def get_matches(telegram_id: int, db: Session = Depends(get_db)):
    me = db.query(models.User).filter(models.User.telegram_id == telegram_id).first()
    if not me:
        raise HTTPException(404, "Пользователь не найден")

    matches = db.query(models.Match).filter(
        (models.Match.user1_id == me.id) | (models.Match.user2_id == me.id)
    ).all()

    result = []
    for match in matches:
        partner_id = match.user2_id if match.user1_id == me.id else match.user1_id
        partner = db.query(models.User).filter(models.User.id == partner_id).first()
        if not partner:
            continue

        last_msg = (
            db.query(models.Message)
            .filter(models.Message.match_id == match.id)
            .order_by(models.Message.created_at.desc())
            .first()
        )

        result.append({
            "match_id": match.id,
            "partner_id": partner.id,
            "pseudonym": partner.pseudonym,
            "age": partner.age,
            "city": partner.city,
            "photos": partner.photos,
            "compatibility_score": match.compatibility_score,
            "last_message": last_msg.text if last_msg else None,
            "expires_at": match.expires_at.isoformat() if match.expires_at else None,
            "created_at": match.created_at.isoformat(),
        })

    return {"matches": result}


def _build_compat_profile_from_user(user: models.User) -> dict:
    profile = user.profile
    if not profile:
        return {"city": user.city}
    return {
        "life_path_number": profile.life_path_number,
        "zodiac_sign": profile.zodiac_sign,
        "moon_sign": profile.moon_sign,
        "hd_type": profile.hd_type,
        "matrix_key_number": profile.matrix_key_number,
        "psychotype": profile.psychotype,
        "attachment_style": profile.attachment_style,
        "love_language_primary": profile.love_language_primary,
        "enneagram_type": profile.enneagram_type,
        "values_score": 70,
        "city": user.city,
    }
