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
from bot.services.vaqt_xizmat import CHEGARA_NOMI, NAMOZ_TARTIBI, NOM_KORSATISH, TZ, hozir

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


async def _kunlik_vaqt(shahar_id: int, sana) -> NamozVaqti | None:
    async with async_session() as s:
        natija = await s.execute(
            select(NamozVaqti).where(NamozVaqti.shahar_id == shahar_id, NamozVaqti.sana == sana)
        )
        return natija.scalar_one_or_none()


async def _chegara_vaqti(shahar_id: int, nom: str, bugun: NamozVaqti, sana) -> datetime | None:
    """Berilgan namoz vaqti tugab, keyingisi kirguvchi vaqt (Xufton uchun
    ertangi Bomdod kerak bo'ladi)."""
    if nom == "xufton":
        ertaga = await _kunlik_vaqt(shahar_id, sana + timedelta(days=1))
        return datetime.combine(ertaga.sana, ertaga.bomdod, tzinfo=TZ) if ertaga else None
    return datetime.combine(sana, getattr(bugun, CHEGARA_NOMI[nom]), tzinfo=TZ)


def _band_id(telegram_id: int, nom: str, turi: str, sana) -> str:
    return f"eslatma_{turi}:{telegram_id}:{nom}:{sana}"


async def _foydalanuvchini_rejala(bot: Bot, f: Foydalanuvchi | None, hoz: datetime, bugun_kesh: dict) -> None:
    """Bitta foydalanuvchining bugungi barcha eslatmalarini (boshlanish
    va tugash) qayta rejalashtiradi — kerak bo'lmagan ishlarni olib tashlaydi."""
    if _scheduler is None or f is None:
        return

    sana = hoz.date()
    if f.shahar_id is not None and f.shahar_id not in bugun_kesh:
        bugun_kesh[f.shahar_id] = await _kunlik_vaqt(f.shahar_id, sana)
    bugun = bugun_kesh.get(f.shahar_id)

    tanlangan = set(f.eslatma_namozlar.split(",")) if f.eslatma_namozlar else set()

    for nom in NAMOZ_TARTIBI:
        boshlanish_id = _band_id(f.telegram_id, nom, "boshlanish", sana)
        tugash_id = _band_id(f.telegram_id, nom, "tugash", sana)

        boshlanish_kerak = bool(f.eslatma_yoqilgan and bugun and nom in tanlangan)
        tugash_kerak = bool(f.eslatma_yoqilgan and f.eslatma_tugash_yoqilgan and bugun and nom in tanlangan)

        if boshlanish_kerak:
            namoz_vaqti = datetime.combine(sana, getattr(bugun, nom), tzinfo=TZ)
            eslatma_vaqti = namoz_vaqti - timedelta(minutes=f.eslatma_daqiqa)
            if eslatma_vaqti > hoz:
                _scheduler.add_job(
                    _boshlanish_yubor, DateTrigger(run_date=eslatma_vaqti),
                    args=[bot, f.telegram_id, nom, namoz_vaqti.strftime("%H:%M")],
                    id=boshlanish_id, replace_existing=True,
                )
            elif _scheduler.get_job(boshlanish_id):
                _scheduler.remove_job(boshlanish_id)
        elif _scheduler.get_job(boshlanish_id):
            _scheduler.remove_job(boshlanish_id)

        chegara_vaqt = await _chegara_vaqti(f.shahar_id, nom, bugun, sana) if tugash_kerak and bugun else None
        if tugash_kerak and chegara_vaqt:
            tugash_vaqti = chegara_vaqt - timedelta(minutes=f.eslatma_tugash_daqiqa)
            if tugash_vaqti > hoz:
                _scheduler.add_job(
                    _tugash_yubor, DateTrigger(run_date=tugash_vaqti),
                    args=[bot, f.telegram_id, nom, CHEGARA_NOMI[nom], chegara_vaqt.strftime("%H:%M")],
                    id=tugash_id, replace_existing=True,
                )
            elif _scheduler.get_job(tugash_id):
                _scheduler.remove_job(tugash_id)
        elif _scheduler.get_job(tugash_id):
            _scheduler.remove_job(tugash_id)


async def bugungi_eslatmalarni_reja(bot: Bot) -> None:
    """Har kuni 00:05 da (va bot ishga tushganda) bugungi barcha
    eslatmalarni APScheduler navbatiga qo'yadi."""
    if _scheduler is None:
        return
    hoz = hozir()
    bugun_kesh: dict[int, NamozVaqti | None] = {}
    foydalanuvchilar = await _faol_foydalanuvchilar()
    for f in foydalanuvchilar:
        await _foydalanuvchini_rejala(bot, f, hoz, bugun_kesh)
    logger.info("Bugungi eslatmalar rejalashtirildi: %d foydalanuvchi", len(foydalanuvchilar))


async def bitta_foydalanuvchi_uchun_reja(bot: Bot, telegram_id: int) -> None:
    """Foydalanuvchi /bildirishnoma orqali sozlamasini o'zgartirganda,
    keyingi kunlik rejani kutmasdan darhol shu kishi uchun qayta rejalaydi."""
    if _scheduler is None:
        return
    async with async_session() as s:
        f = await s.scalar(select(Foydalanuvchi).where(Foydalanuvchi.telegram_id == telegram_id))
    await _foydalanuvchini_rejala(bot, f, hozir(), {})


async def _yuborishga_urin(bot: Bot, telegram_id: int, matn: str) -> None:
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


async def _boshlanish_yubor(bot: Bot, telegram_id: int, namoz_nomi: str, vaqt_matni: str) -> None:
    matn = (
        f"⏰ {NOM_KORSATISH[namoz_nomi]} namozi {vaqt_matni} da — tayyorlanish vaqti keldi.\n\n"
        "Namoz vaqtlari manbasi: namozvaqti.uz — «Book Media Nashr» taqvim kitobi asosida"
    )
    await _yuborishga_urin(bot, telegram_id, matn)


async def _tugash_yubor(
    bot: Bot, telegram_id: int, namoz_nomi: str, chegara_nomi: str, chegara_vaqt_matni: str
) -> None:
    matn = (
        f"⚠️ Diqqat! <b>{NOM_KORSATISH[namoz_nomi]}</b> vaqti tugayapti — "
        f"<b>{NOM_KORSATISH[chegara_nomi]}</b> {chegara_vaqt_matni} da kiradi. "
        "Hali o'qimagan bo'lsangiz, qazo qilib qo'ymang!\n\n"
        "Namoz vaqtlari manbasi: namozvaqti.uz — «Book Media Nashr» taqvim kitobi asosida"
    )
    await _yuborishga_urin(bot, telegram_id, matn)
