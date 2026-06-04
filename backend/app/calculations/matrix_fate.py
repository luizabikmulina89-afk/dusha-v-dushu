MATRIX_ARCHETYPES = {
    1: "Лидер", 2: "Жрица", 3: "Императрица", 4: "Император",
    5: "Иерофант", 6: "Влюблённые", 7: "Колесница", 8: "Сила",
    9: "Отшельник", 10: "Колесо Фортуны", 11: "Справедливость",
    12: "Повешенный", 13: "Смерть (Трансформация)", 14: "Умеренность",
    15: "Дьявол (Материя)", 16: "Башня", 17: "Звезда",
    18: "Луна", 19: "Солнце", 20: "Суд", 21: "Мир", 22: "Шут"
}

MATRIX_COMPAT = {
    (1, 10): 90, (2, 11): 88, (3, 12): 70, (4, 13): 65,
    (5, 14): 85, (6, 15): 60, (7, 16): 70, (8, 17): 82,
    (9, 18): 80, (1, 19): 88, (2, 20): 75, (3, 21): 85,
}


def _reduce_to_22(n: int) -> int:
    while n > 22:
        n = sum(int(d) for d in str(n))
    return n if n > 0 else 22


def calculate_matrix_fate(birth_date: str) -> dict:
    try:
        parts = birth_date.strip().split('.')
        day, month = int(parts[0]), int(parts[1])
        raw = day + month
        key = _reduce_to_22(raw)
        return {
            "key_number": key,
            "archetype": MATRIX_ARCHETYPES.get(key, "Уникальный"),
        }
    except Exception:
        return {"key_number": 1, "archetype": "Лидер"}


def matrix_compatibility(n1: int, n2: int) -> int:
    for key, score in MATRIX_COMPAT.items():
        if set(key) == {n1, n2}:
            return score
    diff = abs(n1 - n2)
    if diff == 0:
        return 72
    if diff <= 3:
        return 80
    if diff <= 7:
        return 70
    return 60
