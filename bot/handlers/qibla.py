from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.services.foydalanuvchi_xizmat import olish
from bot.services.qibla_xizmat import shahar_boyicha
from bot.services.shahar_xizmat import bittasi

router = Router()


@router.message(Command("qibla"))
async def qibla_korsat(message: Message) -> None:
    foydalanuvchi = await olish(message.from_user.id)
    if not foydalanuvchi or not foydalanuvchi.shahar_id:
        await message.answer("Avval shahringizni tanlang: /start")
        return

    shahar = await bittasi(foydalanuvchi.shahar_id)
    malumot = shahar_boyicha(shahar.slug) if shahar else None
    if malumot is None:
        await message.answer("Kechirasiz, bu shahar uchun qibla ma'lumoti hali qo'shilmagan.")
        return

    await message.answer(
        f"🧭 <b>{shahar.nom}</b> uchun qibla yo'nalishi\n\n"
        f"📐 Azimut: <b>{malumot['gradus']}°</b>\n"
        f"🧿 Taxminan: <b>{malumot['yonalish']}</b> tomon\n\n"
        "Kompasda shimolni topib, undan soat strelkasi bo'yicha shu gradusga buriling.\n\n"
        "<i>Bu taxminiy hisob — aniq yo'nalish uchun mahalliy masjid yoki "
        "mo'tabar manbaga murojaat qiling.</i>"
    )
