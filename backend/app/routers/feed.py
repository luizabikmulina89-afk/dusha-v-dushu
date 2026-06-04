from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.calculations.compatibility import calculate_compatibility, apply_proximity_factor

router = APIRouter(prefix="/feed", tags=["feed"])

FREE_DAILY_LIMIT = 10
MIN_COMPATIBILITY = 50


@router.get("/{telegram_id}")
def get_feed(
    telegram_id: int,
    limit: int = Query(default=20, le=50),
    db: Session = Depends(get_db)
):
    me = db.query(models.User).filter(models.User.telegram_id == telegram_id).first()
    if not me or not me.profile:
        return {"candidates": [], "error": "Профиль не заполнен"}

    liked_ids = {like.to_user_id for like in me.sent_likes}

    candidates = (
        db.query(models.User)
        .join(models.UserProfile)
        .filter(
            models.User.id != me.id,
            models.User.is_active == True,
            models.User.is_paused == False,
        )
        .all()
    )

    results = []
    for candidate in candidates:
        if candidate.id in liked_ids:
            continue

        if not _passes_hard_filters(me, candidate):
            continue

        if me.pref_gender and me.pref_gender != "any" and candidate.gender != me.pref_gender:
            continue
        if candidate.age < me.pref_age_min or candidate.age > me.pref_age_max:
            continue

        compat = _build_compat_profile(candidate.profile)
        my_compat = _build_compat_profile(me.profile)
        result = calculate_compatibility(my_compat, compat)

        if result["total"] is None or result["total"] < MIN_COMPATIBILITY:
            continue

        display_score = apply_proximity_factor(result["total"], me.city, candidate.city)

        results.append({
            "user_id": candidate.id,
            "pseudonym": candidate.pseudonym,
            "age": candidate.age,
            "city": candidate.city,
            "photos": candidate.photos,
            "zodiac_sign": candidate.profile.zodiac_sign if candidate.profile else None,
            "hd_type": candidate.profile.hd_type if candidate.profile else None,
            "compatibility_score": display_score,
            "systems_used": result["systems_used"],
        })

    results.sort(key=lambda x: x["compatibility_score"], reverse=True)
    return {"candidates": results[:limit]}


def _passes_hard_filters(me: models.User, candidate: models.User) -> bool:
    if me.wants_children and candidate.wants_children:
        incompatible = {
            ("want", "dont_want"), ("dont_want", "want"),
            ("have_want_more", "dont_want"), ("dont_want", "have_want_more"),
        }
        if (me.wants_children, candidate.wants_children) in incompatible:
            return False

    if me.pref_relation_type and candidate.pref_relation_type:
        if "unsure" not in [me.pref_relation_type, candidate.pref_relation_type]:
            if me.pref_relation_type != candidate.pref_relation_type:
                return False

    if me.religion_partner == "same" and me.religion_own != candidate.religion_own:
        return False
    if candidate.religion_partner == "same" and candidate.religion_own != me.religion_own:
        return False

    return True


def _build_compat_profile(profile: models.UserProfile) -> dict:
    if not profile:
        return {}
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
        "city": profile.user.city if profile.user else None,
    }
