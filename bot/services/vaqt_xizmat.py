from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from sqlalchemy import select

from bot.config import settings
from bot.db.connection import async_session
from bot.db.models import NamozVaqti

TZ = ZoneInfo(settings.timezone)

NAMOZ_TARTIBI = ["bomdod", "peshin", "asr", "shom", "xufton"]
NOM_KORSATISH = {
    "bomdod": "Bomdod", "quyosh": "Quyosh", "peshin": "Peshin",
    "asr": "Asr", "shom": "Shom", "xufton": "Xufton",
}

# Har bir namoz vaqti qaysi chegara bilan tugashini bildiradi — "tugash
# ogohlantirishi" bildirishnomasi uchun (eslatma_xizmat.py).
CHEGARA_NOMI = {"bomdod": "quyosh", "peshin": "asr", "asr": "shom", "shom": "xufton", "xufton": "bomdod"}

# Fiqh: har bir namoz o'z vaqti kirgandan keyingi chegara kirguncha
# amal qiladi (Bomdod -> Quyosh chiqquncha, Peshin -> Asr kirguncha,
# ... Xufton -> ertangi Bomdodgacha). Quyosh bilan Peshin orasida
# hech qaysi farz namozning vaqti faol emas — bu holat joriy_nom=None
# bilan ifodalanadi (keyingi namoz kutilmoqda).
_OYNALAR: list[tuple[str | None, str | None]] = [
    (None, "bomdod"),
    ("bomdod", "quyosh"),
    (None, "peshin"),
    ("peshin", "asr"),
    ("asr", "shom"),
    ("shom", "xufton"),
    ("xufton", None),
]


def hozir() -> datetime:
    return datetime.now(TZ)


async def kunlik_vaqt(shahar_id: int, sana: date) -> NamozVaqti | None:
    async with async_session() as s:
        natija = await s.execute(
            select(NamozVaqti).where(NamozVaqti.shahar_id == shahar_id, NamozVaqti.sana == sana)
        )
        return natija.scalar_one_or_none()


async def joriy_holat(shahar_id: int) -> dict:
    """Hozir qaysi namozning vaqti ichidamiz (yoki keyingisi kutilmoqda)
    va shu oynaning tugash chegarasiga qancha qolganini hisoblaydi.

    Misol: hozir Peshin bilan Asr orasida bo'lsa -> joriy_nom="peshin",
    chegara_nom="asr" (Peshin vaqti Asr kirguncha davom etadi)."""
    hoz = hozir()
    bugun = await kunlik_vaqt(shahar_id, hoz.date())
    if bugun is None:
        return {"topildi": False}

    for joriy_nom, chegara_nom in _OYNALAR:
        if chegara_nom is None:
            # Xufton kirgan — ertangi Bomdodgacha davom etadi.
            ertaga = await kunlik_vaqt(shahar_id, hoz.date() + timedelta(days=1))
            chegara_vaqt = (
                datetime.combine(ertaga.sana, ertaga.bomdod, tzinfo=TZ) if ertaga else None
            )
            return {
                "topildi": True,
                "bugun": bugun,
                "joriy_nom": joriy_nom,
                "chegara_nom": "bomdod",
                "qolgan": (chegara_vaqt - hoz) if chegara_vaqt else None,
            }

        chegara_vaqt = datetime.combine(hoz.date(), getattr(bugun, chegara_nom), tzinfo=TZ)
        if chegara_vaqt > hoz:
            return {
                "topildi": True,
                "bugun": bugun,
                "joriy_nom": joriy_nom,
                "chegara_nom": chegara_nom,
                "qolgan": chegara_vaqt - hoz,
            }

    return {"topildi": False}
