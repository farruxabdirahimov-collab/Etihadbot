from fastapi import APIRouter, Depends, Query
from sqlalchemy import select

from backend.dependencies import joriy_foydalanuvchi
from bot.db.connection import async_session
from bot.db.models import Foydalanuvchi, NamozVaqti, Shahar, Sura
from bot.services.vaqt_xizmat import hozir

router = APIRouter(prefix="/api")


@router.get("/vaqtlar")
async def vaqtlar(shahar_id: int = Query(...)) -> dict:
    async with async_session() as s:
        shahar = await s.get(Shahar, shahar_id)
        natija = await s.execute(
            select(NamozVaqti).where(NamozVaqti.shahar_id == shahar_id, NamozVaqti.sana == hozir().date())
        )
        bugun = natija.scalar_one_or_none()

    if not shahar or not bugun:
        return {"topildi": False}

    return {
        "topildi": True,
        "shahar": shahar.nom,
        "bomdod": bugun.bomdod.strftime("%H:%M"),
        "quyosh": bugun.quyosh.strftime("%H:%M"),
        "peshin": bugun.peshin.strftime("%H:%M"),
        "asr": bugun.asr.strftime("%H:%M"),
        "shom": bugun.shom.strftime("%H:%M"),
        "xufton": bugun.xufton.strftime("%H:%M"),
    }


@router.get("/foydalanuvchi")
async def foydalanuvchi_profil(tg_user: dict = Depends(joriy_foydalanuvchi)) -> dict:
    async with async_session() as s:
        natija = await s.execute(select(Foydalanuvchi).where(Foydalanuvchi.telegram_id == tg_user["id"]))
        f = natija.scalar_one_or_none()

    if not f:
        return {"royxatdan_otganmi": False}

    return {
        "royxatdan_otganmi": True,
        "shahar_id": f.shahar_id,
        "maqsad": f.maqsad,
        "daraja": f.daraja,
    }


@router.get("/suralar")
async def suralar_royxati() -> list[dict]:
    async with async_session() as s:
        natija = await s.execute(select(Sura).order_by(Sura.raqam))
        suralar = natija.scalars().all()

    return [
        {
            "raqam": s.raqam,
            "nom_uz": s.nom_uz,
            "nom_ar": s.nom_ar,
            "oyat_soni": s.oyat_soni,
            "daraja": s.daraja,
        }
        for s in suralar
    ]


@router.get("/suralar/{raqam}")
async def sura_detali(raqam: int) -> dict:
    async with async_session() as s:
        sura = await s.get(Sura, raqam)

    if not sura:
        return {"topildi": False}

    return {
        "topildi": True,
        "raqam": sura.raqam,
        "nom_uz": sura.nom_uz,
        "nom_ar": sura.nom_ar,
        "matn": sura.matn,
        "tasdiqlangan": sura.tasdiqlangan,
    }
