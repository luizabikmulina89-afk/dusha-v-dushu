from typing import Optional
from app.calculations.numerology import numerology_compatibility
from app.calculations.astrology import astrology_compatibility
from app.calculations.human_design import hd_compatibility
from app.calculations.matrix_fate import matrix_compatibility
from app.calculations.tests_scoring import (
    attachment_compatibility, love_language_compatibility,
    enneagram_compatibility, psychotype_compatibility
)

WEIGHTS = {
    "values":       0.15,
    "attachment":   0.15,
    "astrology":    0.12,
    "human_design": 0.12,
    "psychotype":   0.12,
    "numerology":   0.10,
    "matrix_fate":  0.10,
    "love_language":0.07,
    "enneagram":    0.07,
}

SCORE_THRESHOLDS = {
    "excellent": 80,
    "good": 65,
    "possible": 50,
}

MOSCOW_CITIES = {"Москва", "Химки", "Балашиха", "Подольск", "Мытищи"}
SPB_CITIES = {"Санкт-Петербург", "Петербург", "Питер", "Пушкин", "Гатчина"}


def _proximity_coefficient(city1: str, city2: str) -> float:
    if not city1 or not city2:
        return 0.75
    if city1.strip() == city2.strip():
        return 1.0
    same_cluster = any(
        city1 in cluster and city2 in cluster
        for cluster in [MOSCOW_CITIES, SPB_CITIES]
    )
    if same_cluster:
        return 0.95
    cis_countries = {"Минск", "Киев", "Алматы", "Ташкент", "Баку", "Ереван", "Тбилиси"}
    if city1 in cis_countries or city2 in cis_countries:
        return 0.60
    return 0.75


def apply_proximity_factor(score: float, city1: str, city2: str) -> int:
    coef = _proximity_coefficient(city1, city2)
    return round(score * coef)


def calculate_compatibility(profile1: dict, profile2: dict) -> dict:
    breakdown = {}

    v1 = profile1.get("values_score")
    v2 = profile2.get("values_score")
    if v1 is not None and v2 is not None:
        breakdown["values"] = round((v1 + v2) / 2)

    a1 = profile1.get("attachment_style")
    a2 = profile2.get("attachment_style")
    if a1 and a2:
        breakdown["attachment"] = attachment_compatibility(a1, a2)

    z1 = profile1.get("zodiac_sign")
    z2 = profile2.get("zodiac_sign")
    if z1 and z2:
        breakdown["astrology"] = astrology_compatibility(z1, z2)

    hd1 = profile1.get("hd_type")
    hd2 = profile2.get("hd_type")
    if hd1 and hd2:
        breakdown["human_design"] = hd_compatibility(hd1, hd2)

    pt1 = profile1.get("psychotype")
    pt2 = profile2.get("psychotype")
    if pt1 and pt2:
        breakdown["psychotype"] = psychotype_compatibility(pt1, pt2)

    lp1 = profile1.get("life_path_number")
    lp2 = profile2.get("life_path_number")
    if lp1 and lp2:
        breakdown["numerology"] = numerology_compatibility(lp1, lp2)

    m1 = profile1.get("matrix_key_number")
    m2 = profile2.get("matrix_key_number")
    if m1 and m2:
        breakdown["matrix_fate"] = matrix_compatibility(m1, m2)

    ll1 = profile1.get("love_language_primary")
    ll2 = profile2.get("love_language_primary")
    if ll1 and ll2:
        breakdown["love_language"] = love_language_compatibility(ll1, ll2)

    en1 = profile1.get("enneagram_type")
    en2 = profile2.get("enneagram_type")
    if en1 and en2:
        breakdown["enneagram"] = enneagram_compatibility(en1, en2)

    if not breakdown:
        return {"total": None, "breakdown": {}, "systems_used": 0}

    total_weight = sum(WEIGHTS[k] for k in breakdown)
    weighted_sum = sum(breakdown[k] * WEIGHTS[k] for k in breakdown)
    raw_score = weighted_sum / total_weight

    return {
        "total": round(raw_score),
        "breakdown": breakdown,
        "systems_used": len(breakdown),
        "systems_total": 9,
        "label": _score_label(round(raw_score)),
    }


def _score_label(score: int) -> str:
    if score >= SCORE_THRESHOLDS["excellent"]:
        return "Отличная совместимость"
    if score >= SCORE_THRESHOLDS["good"]:
        return "Хорошая совместимость"
    if score >= SCORE_THRESHOLDS["possible"]:
        return "Возможная совместимость"
    return "Низкая совместимость"
