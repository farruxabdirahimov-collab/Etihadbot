import asyncio
import logging
from datetime import datetime, timedelta

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError, TelegramNetworkError
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from sqlalchemy import select

from bot.db.connection import async_session
from bot.db.models import Foydalanuvchi, NamozVaqti
from bot.services.foydalanuvchi_xizmat import ochirish
from bot.services.vaqt_xizmat import NAMOZ_TARTIBI, NOM_KORSATISH, TZ, hozir

logger = logging.getLogger(__name__)

_scheduler: AsyncIOScheduler | None = None


def scheduler_ni_ornat(scheduler: AsyncIOScheduler) -> None:
    global _scheduler
    _scheduler = scheduler


async def _faol_foydalanuvchilar() -> list[Foydalanuvchi]:
    async with async_session() as s:
        natija = await s.execute(
            select(Foydalanuvchi).where(
                Foydalanuvchi.eslatma_yoqilgan.is_(True),
                Foydalanuvchi.shahar_id.is_not(None),
            )
        )
        return list(natija.scalars().all())


async def _bugungi_vaqt(shahar_id: int, sana) -> NamozVaqti | None:
    async with async_session() as s:
        natija = await s.execute(
            select(NamozVaqti).where(NamozVaqti.shahar_id == shahar_id, NamozVaqti.sana == sana)
        )
        return natija.scalar_one_or_none()


async def bugungi_eslatmalarni_reja(bot: Bot) -> None:
    """Har kuni 00:05 da (va bot ishga tushganda) bugungi barcha
    eslatmalarni APScheduler navbatiga qo'yadi."""
    if _scheduler is None:
        return

    foydalanuvchilar = await _faol_foydalanuvchilar()
    hoz = hozir()
    reja_qilindi = 0
    kesh: dict[int, NamozVaqti | None] = {}

    for f in foydalanuvchilar:
        if not f.eslatma_namozlar:
            continue
        if f.shahar_id not in kesh:
            kesh[f.shahar_id] = await _bugungi_vaqt(f.shahar_id, hoz.date())
        bugun = kesh[f.shahar_id]
        if bugun is None:
            continue

        for nom in f.eslatma_namozlar.split(","):
            nom = nom.strip()
            if nom not in NOM_KORSATISH or nom == "quyosh":
                continue
            namoz_vaqti = datetime.combine(hoz.date(), getattr(bugun, nom), tzinfo=TZ)
            eslatma_vaqti = namoz_vaqti - timedelta(minutes=f.eslatma_daqiqa)
            if eslatma_vaqti <= hoz:
                continue

            job_id = f"eslatma:{f.telegram_id}:{nom}:{hoz.date()}"
            _scheduler.add_job(
                _eslatma_yubor,
                DateTrigger(run_date=eslatma_vaqti),
                args=[bot, f.telegram_id, nom, namoz_vaqti.strftime("%H:%M")],
                id=job_id,
                replace_existing=True,
            )
            reja_qilindi += 1

    logger.info("Bugungi eslatmalar rejalashtirildi: %d ta", reja_qilindi)


async def bitta_foydalanuvchi_uchun_reja(bot: Bot, telegram_id: int) -> None:
    """Foydalanuvchi /bildirishnoma orqali sozlamasini o'zgartirganda,
    keyingi kunlik rejani kutmasdan darhol shu kishi uchun qayta rejalaydi
    (yoqadi, o'chiradi yoki vaqtini yangilaydi)."""
    if _scheduler is None:
        return

    async with async_session() as s:
        f = await s.scalar(select(Foydalanuvchi).where(Foydalanuvchi.telegram_id == telegram_id))

    hoz = hozir()
    tanlangan = set(f.eslatma_namozlar.split(",")) if f and f.eslatma_namozlar else set()
    bugun = await _bugungi_vaqt(f.shahar_id, hoz.date()) if f and f.shahar_id else None

    for nom in NAMOZ_TARTIBI:
        job_id = f"eslatma:{telegram_id}:{nom}:{hoz.date()}"
        kerakmi = bool(f and f.eslatma_yoqilgan and nom in tanlangan and bugun is not None)

        if not kerakmi:
            if _scheduler.get_job(job_id):
                _scheduler.remove_job(job_id)
            continue

        namoz_vaqti = datetime.combine(hoz.date(), getattr(bugun, nom), tzinfo=TZ)
        eslatma_vaqti = namoz_vaqti - timedelta(minutes=f.eslatma_daqiqa)
        if eslatma_vaqti <= hoz:
            if _scheduler.get_job(job_id):
                _scheduler.remove_job(job_id)
            continue

        _scheduler.add_job(
            _eslatma_yubor,
            DateTrigger(run_date=eslatma_vaqti),
            args=[bot, telegram_id, nom, namoz_vaqti.strftime("%H:%M")],
            id=job_id,
            replace_existing=True,
        )


async def _eslatma_yubor(bot: Bot, telegram_id: int, namoz_nomi: str, vaqt_matni: str) -> None:
    matn = (
        f"⏰ {NOM_KORSATISH[namoz_nomi]} namozi {vaqt_matni} da — tayyorlanish vaqti keldi.\n\n"
        "Namoz vaqtlari manbasi: namozvaqti.uz — «Book Media Nashr» taqvim kitobi asosida"
    )
    for urinish in range(2):
        try:
            await bot.send_message(telegram_id, matn)
            return
        except TelegramForbiddenError:
            logger.info("Foydalanuvchi botni bloklagan, o'chirilmoqda: %s", telegram_id)
            await ochirish(telegram_id)
            return
        except TelegramNetworkError:
            if urinish == 0:
                await asyncio.sleep(3)
                continue
            logger.warning("Eslatma yuborilmadi (tarmoq xatosi): %s", telegram_id)
