from datetime import date
from pathlib import Path

from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from bot.config import settings
from scraper.sozlamalar import XORAZM, YIRIK_SHAHARLAR
from scraper.suralar import suralarni_yukla
from scraper.vaqtlar import vaqtlarni_yig

_TOPLAMLAR = {
    "xorazm": XORAZM,
    "yirik": YIRIK_SHAHARLAR,
    "hammasi": XORAZM + YIRIK_SHAHARLAR,
}

router = Router()

# Bir vaqtda faqat bitta yig'ish jarayoni ishlasin — tugmani bir necha
# marta bosib yuborilsa ham, ikkinchi jarayon boshlanmaydi.
_band = False


def _admin_mi(message: Message) -> bool:
    return bool(settings.admin_id) and message.from_user is not None and message.from_user.id == settings.admin_id


async def _bandmi(message: Message) -> bool:
    if _band:
        await message.answer("⏳ Boshqa yig'ish jarayoni hali tugamadi. Iltimos, natija kelguncha kuting.")
        return True
    return False


def _hisobot_matni(hisobot: dict) -> str:
    muammoli = {slug: xs for slug, xs in hisobot.items() if xs}
    if not muammoli:
        return ""
    qatorlar = [f"{slug}: {len(xs)} ta muammo — {xs[0]}" for slug, xs in muammoli.items()]
    return "\n\n⚠ Muammoli shaharlar:\n" + "\n".join(qatorlar)


@router.message(Command("yigish_vaqtlar"))
async def yigish_vaqtlar(message: Message, command: CommandObject) -> None:
    global _band
    if not _admin_mi(message) or await _bandmi(message):
        return
    toplam = (command.args or "xorazm").strip().lower()
    shaharlar = _TOPLAMLAR.get(toplam)
    if shaharlar is None:
        await message.answer("Foydalanish: /yigish_vaqtlar [xorazm|yirik|hammasi]")
        return
    await message.answer(
        f"«{toplam}» uchun yillik jadval yig'ish boshlandi ({len(shaharlar)} shahar). "
        "Bir necha daqiqa davom etadi..."
    )
    _band = True
    try:
        jami, hisobot = await vaqtlarni_yig(settings.database_url, date.today().year, shaharlar)
        await message.answer(f"✓ Tayyor: {jami} kun bazaga saqlandi.{_hisobot_matni(hisobot)}")
    except Exception as x:
        await message.answer(f"✗ Xato: {x}")
    finally:
        _band = False


@router.message(Command("yigish_shahar"))
async def yigish_shahar(message: Message, command: CommandObject) -> None:
    global _band
    if not _admin_mi(message) or await _bandmi(message):
        return
    slug = (command.args or "").strip().lower()
    if not slug:
        await message.answer("Foydalanish: /yigish_shahar hazorasp")
        return
    await message.answer(f"«{slug}» uchun qayta yig'ish boshlandi...")
    _band = True
    try:
        jami, hisobot = await vaqtlarni_yig(settings.database_url, date.today().year, [slug])
        muammolar = hisobot.get(slug) or []
        matn = f"✓ Tayyor: {jami} kun saqlandi."
        if muammolar:
            matn += "\n\n⚠ Muammolar:\n" + "\n".join(muammolar)
        await message.answer(matn)
    except Exception as x:
        await message.answer(f"✗ Xato: {x}")
    finally:
        _band = False


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
    global _band
    if not _admin_mi(message) or await _bandmi(message):
        return
    await message.answer("Qisqa suralarni alquran.cloud dan yuklash boshlandi...")
    _band = True
    try:
        soni = await suralarni_yukla(settings.database_url, Path("suralar.json"))
        await message.answer(
            f"✓ Tayyor: {soni} sura saqlandi.\n"
            "Diqqat: matnni bosma mushaf bilan solishtirib, "
            "tasdiqlangan = TRUE qilib belgilash kerak."
        )
    except Exception as x:
        await message.answer(f"✗ Xato: {x}")
    finally:
        _band = False
