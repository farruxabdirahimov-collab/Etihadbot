from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from sqlalchemy import select

from backend.dependencies import joriy_foydalanuvchi
from bot.db.connection import async_session
from bot.db.models import Foydalanuvchi
from bot.services.eslatma_xizmat import bitta_foydalanuvchi_uchun_reja
from bot.services.foydalanuvchi_xizmat import olish
from bot.services.shahar_xizmat import mavjud_shaharlar
from bot.viloyatlar import VILOYAT_TARTIBI, VILOYATLAR

router = APIRouter(prefix="/api")


@router.get("/viloyatlar")
async def viloyatlar_royxati() -> list[dict]:
    """Bugungi ma'lumoti bor shaharlar, viloyatlar bo'yicha guruhlangan
    (Mini App'dagi shahar tanlash ekrani uchun)."""
    shaharlar = await mavjud_shaharlar()
    natija = []
    for nom in VILOYAT_TARTIBI:
        sluglar = VILOYATLAR[nom]
        shu_viloyat = [{"id": sh.id, "nom": sh.nom} for sh in shaharlar if sh.slug in sluglar]
        if shu_viloyat:
            natija.append({"nom": nom, "shaharlar": shu_viloyat})
    return natija


class SozlamaYangilash(BaseModel):
    shahar_id: int | None = None
    eslatma_yoqilgan: bool | None = None
    eslatma_namozlar: list[str] | None = None
    eslatma_daqiqa: int | None = None
    eslatma_tugash_yoqilgan: bool | None = None
    eslatma_tugash_daqiqa: int | None = None


@router.get("/sozlamalar")
async def sozlamalarni_ol(tg_user: dict = Depends(joriy_foydalanuvchi)) -> dict:
    f = await olish(tg_user["id"])
    if not f:
        return {"royxatdan_otganmi": False}
    return {
        "royxatdan_otganmi": True,
        "shahar_id": f.shahar_id,
        "eslatma_yoqilgan": f.eslatma_yoqilgan,
        "eslatma_namozlar": f.eslatma_namozlar.split(",") if f.eslatma_namozlar else [],
        "eslatma_daqiqa": f.eslatma_daqiqa,
        "eslatma_tugash_yoqilgan": f.eslatma_tugash_yoqilgan,
        "eslatma_tugash_daqiqa": f.eslatma_tugash_daqiqa,
    }


@router.patch("/sozlamalar")
async def sozlamalarni_yangila(
    body: SozlamaYangilash, so_rov: Request, tg_user: dict = Depends(joriy_foydalanuvchi)
) -> dict:
    telegram_id = tg_user["id"]

    async with async_session() as s:
        f = await s.scalar(select(Foydalanuvchi).where(Foydalanuvchi.telegram_id == telegram_id))
        if not f:
            return {"royxatdan_otganmi": False}

        if body.shahar_id is not None:
            f.shahar_id = body.shahar_id
        if body.eslatma_yoqilgan is not None:
            f.eslatma_yoqilgan = body.eslatma_yoqilgan
        if body.eslatma_namozlar is not None:
            f.eslatma_namozlar = ",".join(body.eslatma_namozlar)
        if body.eslatma_daqiqa is not None:
            f.eslatma_daqiqa = body.eslatma_daqiqa
        if body.eslatma_tugash_yoqilgan is not None:
            f.eslatma_tugash_yoqilgan = body.eslatma_tugash_yoqilgan
        if body.eslatma_tugash_daqiqa is not None:
            f.eslatma_tugash_daqiqa = body.eslatma_tugash_daqiqa
        await s.commit()

    # Bot bilan bitta protsessda ishlaganimiz uchun eslatmalarni darhol
    # qayta rejalashtiramiz — kunlik 00:05 rejasini kutish shart emas.
    bot = getattr(so_rov.app.state, "bot", None)
    if bot is not None:
        await bitta_foydalanuvchi_uchun_reja(bot, telegram_id)

    return {"royxatdan_otganmi": True}
