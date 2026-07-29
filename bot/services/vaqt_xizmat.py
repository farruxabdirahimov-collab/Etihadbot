from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from sqlalchemy import select

from bot.config import settings
from bot.db.connection import async_session
from bot.db.models import NamozVaqti

TZ = ZoneInfo(settings.timezone)

# Qasr/Quyosh navbatga kirmaydi — foydalanuvchi kutadigan 5 farz namoz.
NAMOZ_TARTIBI = ["bomdod", "peshin", "asr", "shom", "xufton"]
NOM_KORSATISH = {
    "bomdod": "Bomdod", "quyosh": "Quyosh", "peshin": "Peshin",
    "asr": "Asr", "shom": "Shom", "xufton": "Xufton",
}


def hozir() -> datetime:
    return datetime.now(TZ)


async def kunlik_vaqt(shahar_id: int, sana: date) -> NamozVaqti | None:
    async with async_session() as s:
        natija = await s.execute(
            select(NamozVaqti).where(NamozVaqti.shahar_id == shahar_id, NamozVaqti.sana == sana)
        )
        return natija.scalar_one_or_none()


async def joriy_holat(shahar_id: int) -> dict:
    """Bugungi 6 vaqt va keyingi namozgacha qolgan vaqtni hisoblaydi."""
    hoz = hozir()
    bugun = await kunlik_vaqt(shahar_id, hoz.date())
    if bugun is None:
        return {"topildi": False}

    keyingi_nom = None
    keyingi_vaqt = None
    for nom in NAMOZ_TARTIBI:
        toliq = datetime.combine(hoz.date(), getattr(bugun, nom), tzinfo=TZ)
        if toliq > hoz:
            keyingi_nom, keyingi_vaqt = nom, toliq
            break

    if keyingi_nom is None:
        ertaga = await kunlik_vaqt(shahar_id, hoz.date() + timedelta(days=1))
        if ertaga is not None:
            keyingi_nom = "bomdod"
            keyingi_vaqt = datetime.combine(ertaga.sana, ertaga.bomdod, tzinfo=TZ)

    return {
        "topildi": True,
        "bugun": bugun,
        "keyingi_nom": keyingi_nom,
        "qolgan": (keyingi_vaqt - hoz) if keyingi_vaqt else None,
    }
