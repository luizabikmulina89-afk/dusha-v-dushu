from collections import Counter
from typing import List

ATTACHMENT_COMPAT = {
    ("secure", "secure"): 95,
    ("secure", "anxious"): 75,
    ("secure", "avoidant"): 70,
    ("anxious", "anxious"): 45,
    ("anxious", "avoidant"): 30,
    ("avoidant", "avoidant"): 52,
}

LOVE_LANGUAGE_COMPAT = {
    ("words", "words"): 85,   ("words", "acts"): 70,
    ("words", "time"): 75,    ("words", "gifts"): 65,
    ("words", "touch"): 70,   ("acts", "acts"): 85,
    ("acts", "time"): 80,     ("acts", "gifts"): 70,
    ("acts", "touch"): 75,    ("time", "time"): 90,
    ("time", "gifts"): 70,    ("time", "touch"): 80,
    ("gifts", "gifts"): 80,   ("gifts", "touch"): 70,
    ("touch", "touch"): 90,
}

ENNEAGRAM_COMPAT = {
    (1, 2): 72, (1, 7): 78, (1, 9): 85,
    (2, 3): 70, (2, 4): 80, (2, 8): 68,
    (3, 6): 70, (3, 9): 82,
    (4, 5): 85, (4, 9): 75,
    (5, 6): 72, (5, 9): 78,
    (6, 7): 70, (6, 9): 82,
    (7, 8): 75, (7, 9): 80,
    (8, 9): 85,
}


def score_psychotype(answers: List[str]) -> str:
    counts = Counter(answers)
    e_or_i = 'E' if counts.get('E', 0) >= counts.get('I', 0) else 'I'
    s_or_n = 'S' if counts.get('S', 0) >= counts.get('N', 0) else 'N'
    t_or_f = 'T' if counts.get('T', 0) >= counts.get('F', 0) else 'F'
    j_or_p = 'J' if counts.get('J', 0) >= counts.get('P', 0) else 'P'
    return f"{e_or_i}{s_or_n}{t_or_f}{j_or_p}"


def score_attachment(answers: List[str]) -> str:
    counts = Counter(answers)
    return counts.most_common(1)[0][0]


def score_love_language(answers: List[str]) -> str:
    counts = Counter(answers)
    return counts.most_common(1)[0][0]


def score_enneagram(answers: List[int]) -> int:
    counts = Counter(answers)
    return counts.most_common(1)[0][0]


def attachment_compatibility(style1: str, style2: str) -> int:
    key = (style1, style2)
    if key in ATTACHMENT_COMPAT:
        return ATTACHMENT_COMPAT[key]
    key_rev = (style2, style1)
    return ATTACHMENT_COMPAT.get(key_rev, 60)


def love_language_compatibility(lang1: str, lang2: str) -> int:
    key = (lang1, lang2)
    if key in LOVE_LANGUAGE_COMPAT:
        return LOVE_LANGUAGE_COMPAT[key]
    key_rev = (lang2, lang1)
    return LOVE_LANGUAGE_COMPAT.get(key_rev, 70)


def enneagram_compatibility(type1: int, type2: int) -> int:
    if type1 == type2:
        return 68
    key = (min(type1, type2), max(type1, type2))
    return ENNEAGRAM_COMPAT.get(key, 65)


def psychotype_compatibility(mbti1: str, mbti2: str) -> int:
    if mbti1 == mbti2:
        return 65
    opposites_good = {("INTJ", "ENFP"), ("INFJ", "ENTP"), ("ISTJ", "ESFP"),
                      ("ISFJ", "ESTP"), ("INTP", "ENTJ"), ("INFP", "ENFJ")}
    if (mbti1, mbti2) in opposites_good or (mbti2, mbti1) in opposites_good:
        return 88
    matches = sum(a == b for a, b in zip(mbti1, mbti2))
    if matches == 3:
        return 80
    if matches == 2:
        return 72
    if matches == 1:
        return 65
    return 60
