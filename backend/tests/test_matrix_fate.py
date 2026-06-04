from app.calculations.matrix_fate import calculate_matrix_fate, matrix_compatibility

def test_matrix_returns_key_number():
    result = calculate_matrix_fate("15.03.1990")
    assert "key_number" in result
    assert 1 <= result["key_number"] <= 22

def test_matrix_deterministic():
    r1 = calculate_matrix_fate("01.01.1990")
    r2 = calculate_matrix_fate("01.01.1990")
    assert r1["key_number"] == r2["key_number"]

def test_matrix_compatibility_range():
    score = matrix_compatibility(7, 3)
    assert 0 <= score <= 100
