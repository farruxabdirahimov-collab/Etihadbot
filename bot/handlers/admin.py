from datetime import date
from pathlib import Path

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.config import settings
from scraper.sozlamalar import XORAZM
from scraper.suralar import suralarni_yukla
from scraper.vaqtlar import vaqtlarni_yig

router = Router()


def _admin_mi(message: Message) -> bool:
    return bool(settings.admin_id) and message.from_user is not None and message.from_user.id == settings.admin_id


@router.message(Command("yigish_vaqtlar"))
async def yigish_vaqtlar(message: Message) -> None:
    if not _admin_mi(message):
        return
    await message.answer("Xorazm (6 shahar) uchun yillik jadval yig'ish boshlandi. Bir necha daqiqa davom etadi...")
    try:
        jami = await vaqtlarni_yig(settings.database_url, date.today().year, XORAZM)
        await message.answer(f"✓ Tayyor: {jami} kun bazaga saqlandi.")
    except Exception as x:
        await message.answer(f"✗ Xato: {x}")


@router.message(Command("tekshir"))
async def tekshir(message: Message) -> None:
    if not _admin_mi(message):
        return
    import asyncpg

    conn = await asyncpg.connect(settings.database_url)
    try:
        qatorlar = await conn.fetch(
            """SELECT sh.nom, COUNT(v.id) AS soni
               FROM shaharlar sh
               LEFT JOIN namoz_vaqtlari v ON v.shahar_id = sh.id
               GROUP BY sh.nom
               ORDER BY sh.nom"""
        )
        sura_soni = await conn.fetchval("SELECT COUNT(*) FROM suralar")
    finally:
        await conn.close()

    matn = "\n".join(f"{r['nom']}: {r['soni']} kun" for r in qatorlar)
    await message.answer(f"Shaharlar bo'yicha:\n{matn}\n\nSuralar: {sura_soni} ta")


@router.message(Command("yigish_suralar"))
async def yigish_suralar(message: Message) -> None:
    if not _admin_mi(message):
        return
    await message.answer("Qisqa suralarni alquran.cloud dan yuklash boshlandi...")
    try:
        soni = await suralarni_yukla(settings.database_url, Path("suralar.json"))
        await message.answer(
            f"✓ Tayyor: {soni} sura saqlandi.\n"
            "Diqqat: matnni bosma mushaf bilan solishtirib, "
            "tasdiqlangan = TRUE qilib belgilash kerak."
        )
    except Exception as x:
        await message.answer(f"✗ Xato: {x}")
