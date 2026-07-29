from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from bot.keyboards import shahar_klaviaturasi, viloyat_klaviaturasi
from bot.services.foydalanuvchi_xizmat import olish, shaharni_yangila
from bot.services.shahar_xizmat import bittasi, sluglar_boyicha
from bot.viloyatlar import VILOYAT_TARTIBI, VILOYATLAR

router = Router()


@router.message(Command("sozlama"))
async def sozlama_menyu(message: Message) -> None:
    foydalanuvchi = await olish(message.from_user.id)
    if not foydalanuvchi:
        await message.answer("Avval ro'yxatdan o'ting: /start")
        return

    shahar = await bittasi(foydalanuvchi.shahar_id) if foydalanuvchi.shahar_id else None
    matn = (
        f"Joriy shahar: {shahar.nom if shahar else 'tanlanmagan'}\n\n"
        "Shaharni o'zgartirish uchun viloyatingizni tanlang:"
    )
    await message.answer(matn, reply_markup=viloyat_klaviaturasi(prefix="sviloyat"))


@router.callback_query(F.data.startswith("sviloyat:"))
async def sozlama_viloyat(callback: CallbackQuery) -> None:
    idx = int(callback.data.split(":", 1)[1])
    viloyat_nomi = VILOYAT_TARTIBI[idx]
    sluglar = VILOYATLAR[viloyat_nomi]
    shaharlar = await sluglar_boyicha(sluglar)

    if not shaharlar:
        await callback.answer("Bu viloyatda hozircha ma'lumot yo'q.", show_alert=True)
        return

    if len(shaharlar) == 1:
        await shaharni_yangila(callback.from_user.id, shaharlar[0].id)
        await callback.message.edit_text(f"✓ Shahar yangilandi: {shaharlar[0].nom}")
        await callback.answer()
        return

    await callback.message.edit_text(
        f"{viloyat_nomi} — aniq shahringizni tanlang:",
        reply_markup=shahar_klaviaturasi(shaharlar, prefix="sshahar"),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("sshahar:"))
async def sozlama_shahar(callback: CallbackQuery) -> None:
    shahar_id = int(callback.data.split(":", 1)[1])
    await shaharni_yangila(callback.from_user.id, shahar_id)
    shahar = await bittasi(shahar_id)
    await callback.message.edit_text(f"✓ Shahar yangilandi: {shahar.nom if shahar else '—'}")
    await callback.answer()
