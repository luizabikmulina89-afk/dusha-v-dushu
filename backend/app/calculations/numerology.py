PYTHAGOREAN_RU = {
    'а': 1, 'б': 2, 'в': 6, 'г': 3, 'д': 4, 'е': 5, 'ё': 5,
    'ж': 2, 'з': 7, 'и': 1, 'й': 1, 'к': 2, 'л': 3, 'м': 4,
    'н': 5, 'о': 7, 'п': 8, 'р': 9, 'с': 1, 'т': 2, 'у': 3,
    'ф': 8, 'х': 5, 'ц': 6, 'ч': 7, 'ш': 8, 'щ': 9, 'ъ': 1,
    'ы': 2, 'ь': 3, 'э': 5, 'ю': 6, 'я': 7
}

VOWELS_RU = set('аеёиоуыэюя')
MASTER_NUMBERS = {11, 22, 33}

LIFE_PATH_TITLES = {
    1: "Лидер", 2: "Партнёр", 3: "Творец", 4: "Строитель",
    5: "Искатель", 6: "Хранитель", 7: "Мудрец", 8: "Властитель",
    9: "Гуманист", 11: "Вдохновитель", 22: "Строитель миров", 33: "Учитель"
}

LIFE_PATH_DESC = {
    1: "Рождён вести за собой. Сильные стороны — независимость, воля, амбиции.",
    2: "Чувствуешь людей и умеешь находить баланс. Путь — строить гармоничные отношения.",
    3: "Наполнен творческой энергией. Путь — творчество и радость.",
    4: "Создаёшь прочный фундамент. Путь — стабильность и надёжность.",
    5: "Жаждешь свободы и новых впечатлений. Путь — изменения и разнообразие.",
    6: "Несёшь в мир заботу и гармонию. Путь — служение семье.",
    7: "Ищешь глубинный смысл всего. Путь — познание истины.",
    8: "Рождён управлять. Путь — успех и влияние.",
    9: "Несёшь мудрость и сострадание. Путь — служение человечеству.",
    11: "Особая миссия — вдохновлять и пробуждать в людях высшее.",
    22: "Воплощать великие идеи в реальность. Редкий дар.",
    33: "Высшая любовь и мудрость. Исцелять, учить, поднимать других."
}

NUMEROLOGY_COMPAT = {
    (1, 1): 60, (1, 2): 70, (1, 3): 85, (1, 4): 50, (1, 5): 80,
    (1, 6): 65, (1, 7): 55, (1, 8): 75, (1, 9): 80,
    (2, 2): 65, (2, 3): 70, (2, 4): 80, (2, 5): 60, (2, 6): 90,
    (2, 7): 55, (2, 8): 75, (2, 9): 70,
    (3, 3): 70, (3, 4): 55, (3, 5): 85, (3, 6): 75, (3, 7): 65,
    (3, 8): 60, (3, 9): 90,
    (4, 4): 70, (4, 5): 55, (4, 6): 80, (4, 7): 75, (4, 8): 90,
    (4, 9): 60,
    (5, 5): 65, (5, 6): 55, (5, 7): 80, (5, 8): 65, (5, 9): 75,
    (6, 6): 75, (6, 7): 60, (6, 8): 70, (6, 9): 85,
    (7, 7): 65, (7, 8): 60, (7, 9): 80,
    (8, 8): 60, (8, 9): 65,
    (9, 9): 70,
}


def reduce_to_single(n: int) -> int:
    while n > 9 and n not in MASTER_NUMBERS:
        n = sum(int(d) for d in str(n))
    return n


def calculate_life_path(date_str: str) -> dict:
    try:
        parts = date_str.strip().replace('-', '.').replace('/', '.').split('.')
        if len(parts) != 3:
            return {"error": "Введи дату в формате ДД.ММ.ГГГГ"}
        day, month, year = parts
        day_sum = reduce_to_single(sum(int(d) for d in day.zfill(2)))
        month_sum = reduce_to_single(sum(int(d) for d in month.zfill(2)))
        year_sum = reduce_to_single(sum(int(d) for d in year.zfill(4)))
        total = reduce_to_single(day_sum + month_sum + year_sum)
        return {
            "number": total,
            "title": LIFE_PATH_TITLES.get(total, "Уникальное число"),
            "description": LIFE_PATH_DESC.get(total, ""),
            "breakdown": f"{day_sum} + {month_sum} + {year_sum} → {total}"
        }
    except Exception:
        return {"error": "Неверный формат даты. Используй ДД.ММ.ГГГГ"}


def calculate_destiny(full_name: str) -> dict:
    digits = [PYTHAGOREAN_RU[c] for c in full_name.lower() if c in PYTHAGOREAN_RU]
    if not digits:
        return {"error": "Имя не распознано"}
    total = reduce_to_single(sum(digits))
    return {
        "number": total,
        "title": LIFE_PATH_TITLES.get(total, ""),
        "description": LIFE_PATH_DESC.get(total, "")
    }


def calculate_soul(full_name: str) -> dict:
    digits = [PYTHAGOREAN_RU[c] for c in full_name.lower()
              if c in VOWELS_RU and c in PYTHAGOREAN_RU]
    if not digits:
        return {"error": "Гласные не найдены"}
    total = reduce_to_single(sum(digits))
    return {"number": total}


def calculate_personality_number(full_name: str) -> dict:
    consonants = set(PYTHAGOREAN_RU.keys()) - VOWELS_RU
    digits = [PYTHAGOREAN_RU[c] for c in full_name.lower() if c in consonants]
    if not digits:
        return {"error": "Согласные не найдены"}
    total = reduce_to_single(sum(digits))
    return {"number": total}


def numerology_compatibility(n1: int, n2: int) -> int:
    if n1 == n2:
        return NUMEROLOGY_COMPAT.get((n1, n1), 65)
    key = (min(n1, n2), max(n1, n2))
    return NUMEROLOGY_COMPAT.get(key, 65)
