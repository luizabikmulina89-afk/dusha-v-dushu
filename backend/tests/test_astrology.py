from app.calculations.astrology import (
    get_zodiac_sign,
    get_moon_sign,
    astrology_compatibility,
    ZODIAC_ELEMENTS,
)

def test_zodiac_aries():
    assert get_zodiac_sign(21, 3) == "Овен"

def test_zodiac_leo():
    assert get_zodiac_sign(15, 8) == "Лев"

def test_zodiac_capricorn_january():
    assert get_zodiac_sign(5, 1) == "Козерог"

def test_zodiac_capricorn_december():
    assert get_zodiac_sign(25, 12) == "Козерог"

def test_all_signs_covered():
    for month in range(1, 13):
        result = get_zodiac_sign(15, month)
        assert result is not None and len(result) > 0

def test_zodiac_elements_complete():
    all_signs = ["Овен", "Телец", "Близнецы", "Рак", "Лев", "Дева",
                 "Весы", "Скорпион", "Стрелец", "Козерог", "Водолей", "Рыбы"]
    for sign in all_signs:
        assert sign in ZODIAC_ELEMENTS

def test_fire_air_compatibility_high():
    score = astrology_compatibility("Овен", "Близнецы")
    assert score >= 75

def test_fire_earth_compatibility_lower():
    score = astrology_compatibility("Овен", "Телец")
    assert score <= 65

def test_same_sign_compatibility():
    score = astrology_compatibility("Лев", "Лев")
    assert 50 <= score <= 85
