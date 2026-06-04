from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.schemas import UserCreate, BirthDataUpdate, HardFiltersUpdate, TestAnswerSubmit
from app.calculations.numerology import calculate_life_path, calculate_destiny, calculate_soul
from app.calculations.astrology import get_zodiac_sign, get_moon_sign
from app.calculations.human_design import get_hd_type
from app.calculations.matrix_fate import calculate_matrix_fate
from app.calculations.tests_scoring import (
    score_psychotype, score_attachment, score_love_language, score_enneagram
)

router = APIRouter(prefix="/users", tags=["users"])


def _get_user_or_404(telegram_id: int, db: Session) -> models.User:
    user = db.query(models.User).filter(models.User.telegram_id == telegram_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user


@router.post("/register")
def register_user(data: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.telegram_id == data.telegram_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Пользователь уже зарегистрирован")

    user = models.User(**data.model_dump())
    db.add(user)
    db.flush()

    profile = models.UserProfile(user_id=user.id)
    db.add(profile)
    db.commit()
    db.refresh(user)
    return {"ok": True, "user_id": user.id}


@router.post("/{telegram_id}/birth-data")
def update_birth_data(telegram_id: int, data: BirthDataUpdate, db: Session = Depends(get_db)):
    user = _get_user_or_404(telegram_id, db)
    profile = user.profile

    profile.birth_date = data.birth_date
    profile.birth_time = data.birth_time
    profile.birth_city = data.birth_city

    lp = calculate_life_path(data.birth_date)
    if "number" in lp:
        profile.life_path_number = lp["number"]

    if data.full_name:
        profile.full_name = data.full_name
        dest = calculate_destiny(data.full_name)
        soul = calculate_soul(data.full_name)
        if "number" in dest:
            profile.destiny_number = dest["number"]
        if "number" in soul:
            profile.soul_number = soul["number"]

    parts = data.birth_date.split('.')
    day, month = int(parts[0]), int(parts[1])
    profile.zodiac_sign = get_zodiac_sign(day, month)
    profile.moon_sign = get_moon_sign(data.birth_date, data.birth_time)
    profile.hd_type = get_hd_type(data.birth_date)

    matrix = calculate_matrix_fate(data.birth_date)
    profile.matrix_key_number = matrix["key_number"]

    _update_completed_systems(profile)
    db.commit()
    return {"ok": True, "life_path": profile.life_path_number,
            "zodiac": profile.zodiac_sign, "hd_type": profile.hd_type}


@router.post("/{telegram_id}/hard-filters")
def update_hard_filters(telegram_id: int, data: HardFiltersUpdate, db: Session = Depends(get_db)):
    user = _get_user_or_404(telegram_id, db)
    for field, value in data.model_dump().items():
        setattr(user, field, value)
    db.commit()
    return {"ok": True}


@router.post("/{telegram_id}/test")
def submit_test(telegram_id: int, data: TestAnswerSubmit, db: Session = Depends(get_db)):
    user = _get_user_or_404(telegram_id, db)
    profile = user.profile

    if data.test_type == "psychotype":
        profile.psychotype = score_psychotype(data.answers)
    elif data.test_type == "attachment":
        profile.attachment_style = score_attachment(data.answers)
    elif data.test_type == "love_language":
        profile.love_language_primary = score_love_language(data.answers)
    elif data.test_type == "enneagram":
        profile.enneagram_type = score_enneagram([int(a) for a in data.answers])
    else:
        raise HTTPException(status_code=400, detail="Неизвестный тип теста")

    _update_completed_systems(profile)
    db.commit()
    return {"ok": True, "test_type": data.test_type}


@router.get("/{telegram_id}/profile")
def get_profile(telegram_id: int, db: Session = Depends(get_db)):
    user = _get_user_or_404(telegram_id, db)
    profile = user.profile
    return {
        "pseudonym": user.pseudonym,
        "age": user.age,
        "city": user.city,
        "life_path_number": profile.life_path_number,
        "zodiac_sign": profile.zodiac_sign,
        "hd_type": profile.hd_type,
        "psychotype": profile.psychotype,
        "attachment_style": profile.attachment_style,
        "love_language_primary": profile.love_language_primary,
        "enneagram_type": profile.enneagram_type,
        "completed_systems": profile.completed_systems,
    }


def _update_completed_systems(profile: models.UserProfile):
    count = sum(1 for field in [
        profile.life_path_number, profile.zodiac_sign, profile.hd_type,
        profile.matrix_key_number, profile.psychotype, profile.attachment_style,
        profile.love_language_primary, profile.enneagram_type,
    ] if field is not None)
    profile.completed_systems = count
