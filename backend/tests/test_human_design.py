from app.calculations.human_design import get_hd_type, hd_compatibility

def test_hd_type_returns_valid():
    hd_type = get_hd_type("15.03.1990")
    valid_types = ["Генератор", "Манифестирующий Генератор", "Манифестор", "Проектор", "Рефлектор"]
    assert hd_type in valid_types

def test_hd_type_deterministic():
    assert get_hd_type("01.01.1985") == get_hd_type("01.01.1985")

def test_hd_compatibility_generator_projector():
    score = hd_compatibility("Генератор", "Проектор")
    assert score >= 80

def test_hd_compatibility_range():
    types = ["Генератор", "Манифестирующий Генератор", "Манифестор", "Проектор", "Рефлектор"]
    for t1 in types:
        for t2 in types:
            score = hd_compatibility(t1, t2)
            assert 0 <= score <= 100
