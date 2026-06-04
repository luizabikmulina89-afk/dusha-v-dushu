from typing import Optional

ZODIAC_SIGNS = [
    ("Козерог", 1, 1, 1, 19),
    ("Водолей", 1, 20, 2, 18),
    ("Рыбы", 2, 19, 3, 20),
    ("Овен", 3, 21, 4, 19),
    ("Телец", 4, 20, 5, 20),
    ("Близнецы", 5, 21, 6, 20),
    ("Рак", 6, 21, 7, 22),
    ("Лев", 7, 23, 8, 22),
    ("Дева", 8, 23, 9, 22),
    ("Весы", 9, 23, 10, 22),
    ("Скорпион", 10, 23, 11, 21),
    ("Стрелец", 11, 22, 12, 21),
    ("Козерог", 12, 22, 12, 31),
]

ZODIAC_ELEMENTS = {
    "Овен": "Огонь", "Лев": "Огонь", "Стрелец": "Огонь",
    "Телец": "Земля", "Дева": "Земля", "Козерог": "Земля",
    "Близнецы": "Воздух", "Весы": "Воздух", "Водолей": "Воздух",
    "Рак": "Вода", "Скорпион": "Вода", "Рыбы": "Вода",
}

ELEMENT_COMPAT = {
    ("Огонь", "Огонь"): 72,
    ("Огонь", "Воздух"): 88,
    ("Огонь", "Земля"): 55,
    ("Огонь", "Вода"): 62,
    ("Земля", "Земля"): 75,
    ("Земля", "Вода"): 82,
    ("Земля", "Воздух"): 58,
    ("Воздух", "Воздух"): 73,
    ("Воздух", "Вода"): 65,
    ("Вода", "Вода"): 78,
}


def get_zodiac_sign(day: int, month: int) -> str:
    for sign, m1, d1, m2, d2 in ZODIAC_SIGNS:
        if (month == m1 and day >= d1) or (month == m2 and day <= d2):
            return sign
    return "Козерог"


def get_moon_sign(birth_date: str, birth_time: Optional[str] = None,
                  birth_city: Optional[str] = None) -> Optional[str]:
    try:
        import ephem
        parts = birth_date.strip().split('.')
        day, month, year = int(parts[0]), int(parts[1]), int(parts[2])

        time_str = birth_time if birth_time else "12:00"
        h, m = time_str.split(':')

        dt = ephem.Date(f"{year}/{month}/{day} {h}:{m}:00")
        moon = ephem.Moon(dt)
        moon.compute(dt)

        ecl = ephem.Ecliptic(moon, epoch=dt)
        longitude = float(ecl.lon) * 180 / 3.14159265358979

        signs = ["Овен", "Телец", "Близнецы", "Рак", "Лев", "Дева",
                 "Весы", "Скорпион", "Стрелец", "Козерог", "Водолей", "Рыбы"]
        index = int(longitude / 30) % 12
        return signs[index]
    except Exception:
        return None


def astrology_compatibility(sign1: str, sign2: str) -> int:
    elem1 = ZODIAC_ELEMENTS.get(sign1)
    elem2 = ZODIAC_ELEMENTS.get(sign2)
    if not elem1 or not elem2:
        return 65
    for k in [(elem1, elem2), (elem2, elem1)]:
        if k in ELEMENT_COMPAT:
            return ELEMENT_COMPAT[k]
    return 65
