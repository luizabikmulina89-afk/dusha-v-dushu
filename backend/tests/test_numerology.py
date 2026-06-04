from app.calculations.numerology import (
    calculate_life_path,
    calculate_destiny,
    calculate_soul,
    calculate_personality_number,
    numerology_compatibility,
)

def test_life_path_basic():
    result = calculate_life_path("15.03.1990")
    assert result["number"] == 1  # 1+5+0+3+1+9+9+0 = 28 → 2+8=10 → 1+0=1
    assert "title" in result
    assert "description" in result

def test_life_path_master_number():
    # 03.01.2014: day=3, month=1, year=7 → 3+1+7=11 (master number)
    result = calculate_life_path("03.01.2014")
    assert result["number"] == 11

def test_life_path_invalid_date():
    result = calculate_life_path("неверная дата")
    assert "error" in result

def test_destiny_from_name():
    result = calculate_destiny("Иванова Анна Сергеевна")
    assert isinstance(result["number"], int)
    assert 1 <= result["number"] <= 33

def test_soul_number():
    result = calculate_soul("Иванова Анна Сергеевна")
    assert isinstance(result["number"], int)
    assert 1 <= result["number"] <= 33

def test_numerology_compatibility_same_numbers():
    score = numerology_compatibility(7, 7)
    assert isinstance(score, int)
    assert 0 <= score <= 100

def test_numerology_compatibility_known_pair():
    score = numerology_compatibility(1, 3)
    assert score >= 70
