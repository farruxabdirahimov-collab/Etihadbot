import math

from bot.koordinatalar import SHAHAR_KOORDINATALARI

# Ka'ba koordinatalari (Masjidul Harom, Makka).
KABA_LAT = 21.4225
KABA_LON = 39.8262

# 16 rumb — gradusni o'zbekcha yo'nalish nomiga aylantirish uchun.
_YONALISHLAR = [
    "shimol", "shimoli-shimoli-sharq", "shimoli-sharq", "sharqi-shimoli-sharq",
    "sharq", "sharqi-janubi-sharq", "janubi-sharq", "janubi-janubi-sharq",
    "janub", "janubi-janubi-g'arb", "janubi-g'arb", "g'arbi-janubi-g'arb",
    "g'arb", "g'arbi-shimoli-g'arb", "shimoli-g'arb", "shimoli-shimoli-g'arb",
]


def qibla_burchagi(lat: float, lon: float) -> float:
    """Berilgan nuqtadan Ka'baga qarab katta doira (great circle) bo'yicha
    boshlang'ich azimut — shimoldan soat strelkasi bo'yicha gradusda."""
    p1 = math.radians(lat)
    p2 = math.radians(KABA_LAT)
    dl = math.radians(KABA_LON - lon)

    y = math.sin(dl) * math.cos(p2)
    x = math.cos(p1) * math.sin(p2) - math.sin(p1) * math.cos(p2) * math.cos(dl)
    return (math.degrees(math.atan2(y, x)) + 360) % 360


def yonalish_nomi(gradus: float) -> str:
    return _YONALISHLAR[round(gradus / 22.5) % 16]


def shahar_boyicha(slug: str) -> dict | None:
    """Shahar slug'i bo'yicha qibla ma'lumoti. Koordinatasi yo'q shahar
    uchun None qaytaradi."""
    koordinata = SHAHAR_KOORDINATALARI.get(slug)
    if koordinata is None:
        return None
    lat, lon = koordinata
    gradus = qibla_burchagi(lat, lon)
    return {"gradus": round(gradus, 1), "yonalish": yonalish_nomi(gradus), "lat": lat, "lon": lon}
