from sqlalchemy import select

from bot.db.connection import async_session
from bot.db.models import NamozVaqti, Shahar
from bot.services.vaqt_xizmat import hozir
from scraper.sozlamalar import XORAZM, YIRIK_SHAHARLAR


async def mavjud_shaharlar() -> list[Shahar]:
    """Bugungi sana uchun ma'lumoti bor shaharlar ro'yxati."""
    bugun = hozir().date()
    async with async_session() as s:
        natija = await s.execute(
            select(Shahar)
            .join(NamozVaqti, NamozVaqti.shahar_id == Shahar.id)
            .where(NamozVaqti.sana == bugun)
            .order_by(Shahar.nom)
            .distinct()
        )
        return list(natija.scalars().all())


async def hudud_boyicha(hudud: str) -> list[Shahar]:
    """'xorazm' yoki 'yirik' hududiga tegishli, bugungi ma'lumoti bor shaharlar."""
    slug_royxati = XORAZM if hudud == "xorazm" else YIRIK_SHAHARLAR
    barchasi = await mavjud_shaharlar()
    return [sh for sh in barchasi if sh.slug in slug_royxati]


async def bittasi(shahar_id: int) -> Shahar | None:
    async with async_session() as s:
        return await s.get(Shahar, shahar_id)
