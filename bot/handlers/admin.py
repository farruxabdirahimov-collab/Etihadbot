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
