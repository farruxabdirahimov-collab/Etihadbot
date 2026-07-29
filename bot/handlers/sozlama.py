from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from bot.keyboards import hudud_klaviaturasi, shahar_klaviaturasi
from bot.services.foydalanuvchi_xizmat import olish, shaharni_yangila
from bot.services.shahar_xizmat import bittasi, hudud_boyicha

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
        "Shaharni o'zgartirish uchun hududni tanlang:"
    )
    await message.answer(matn, reply_markup=hudud_klaviaturasi(prefix="shudud"))


@router.callback_query(F.data.startswith("shudud:"))
async def sozlama_hudud(callback: CallbackQuery) -> None:
    hudud = callback.data.split(":", 1)[1]
    shaharlar = await hudud_boyicha(hudud)
    if not shaharlar:
        await callback.answer("Bu hududda hozircha ma'lumot yo'q.", show_alert=True)
        return
    await callback.message.edit_text(
        "Yangi shahringizni tanlang:",
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
