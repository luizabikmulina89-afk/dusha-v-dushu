from app.calculations.compatibility import calculate_compatibility, apply_proximity_factor

def make_profile(**kwargs):
    defaults = {
        "life_path_number": 7, "zodiac_sign": "Лев", "moon_sign": "Рыбы",
        "hd_type": "Генератор", "matrix_key_number": 5,
        "psychotype": "INFJ", "attachment_style": "secure",
        "love_language_primary": "time", "enneagram_type": 4,
        "values_score": 80, "city": "Москва",
    }
    defaults.update(kwargs)
    return defaults

def test_full_compatibility_returns_score():
    p1 = make_profile()
    p2 = make_profile(life_path_number=2, zodiac_sign="Рыбы",
                      hd_type="Проектор", psychotype="ENFP")
    result = calculate_compatibility(p1, p2)
    assert "total" in result
    assert 0 <= result["total"] <= 100

def test_empty_profiles_return_none():
    p1 = make_profile(psychotype=None, attachment_style=None,
                      love_language_primary=None, enneagram_type=None)
    p2 = make_profile(psychotype=None, attachment_style=None,
                      love_language_primary=None, enneagram_type=None)
    result = calculate_compatibility(p1, p2)
    assert result["systems_used"] >= 2

def test_compatibility_breakdown_has_all_keys():
    p1 = make_profile()
    p2 = make_profile()
    result = calculate_compatibility(p1, p2)
    assert "breakdown" in result
    assert "numerology" in result["breakdown"]
    assert "astrology" in result["breakdown"]

def test_proximity_same_city():
    score = apply_proximity_factor(80, "Москва", "Москва")
    assert score == 80

def test_proximity_different_country():
    score = apply_proximity_factor(100, "Москва", "Минск")
    assert score < 100
