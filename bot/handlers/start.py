from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.keyboards import MAQSADLAR, hudud_klaviaturasi, maqsad_klaviaturasi, shahar_klaviaturasi
from bot.services.foydalanuvchi_xizmat import olish, royxatga_ol
from bot.services.shahar_xizmat import bittasi, hudud_boyicha
from bot.states import RoyxatState

router = Router()

MANBA_MATNI = (
    "Namoz vaqtlari manbasi: namozvaqti.uz — "
    "«Book Media Nashr» taqvim kitobi asosida"
)


@router.message(CommandStart())
async def handle_start(message: Message, state: FSMContext) -> None:
    mavjud = await olish(message.from_user.id)
    if mavjud and mavjud.shahar_id:
        shahar = await bittasi(mavjud.shahar_id)
        await message.answer(
            f"Assalomu alaykum! Siz allaqachon ro'yxatdan o'tgansiz — "
            f"shahringiz: {shahar.nom if shahar else '—'}.\n\n"
            "Bugungi namoz vaqtlari uchun /vaqt, sozlamalarni o'zgartirish uchun "
            "/sozlama yuboring.\n\n"
            f"{MANBA_MATNI}"
        )
        return

    await state.set_state(RoyxatState.maqsad)
    await message.answer(
        "Assalomu alaykum! Namoz Bot'ga xush kelibsiz.\n\n"
        "Botdan maqsadingiz nima?",
        reply_markup=maqsad_klaviaturasi(),
    )


@router.callback_query(RoyxatState.maqsad, F.data.startswith("maqsad:"))
async def maqsad_tanlandi(callback: CallbackQuery, state: FSMContext) -> None:
    maqsad = callback.data.split(":", 1)[1]
    await state.update_data(maqsad=maqsad)
    await state.set_state(RoyxatState.hudud)
    await callback.message.edit_text(
        f"Tanlandi: {MAQSADLAR[maqsad]}\n\nEndi hududingizni tanlang:",
        reply_markup=hudud_klaviaturasi(),
    )
    await callback.answer()


@router.callback_query(RoyxatState.hudud, F.data.startswith("hudud:"))
async def hudud_tanlandi(callback: CallbackQuery, state: FSMContext) -> None:
    hudud = callback.data.split(":", 1)[1]
    shaharlar = await hudud_boyicha(hudud)
    if not shaharlar:
        await callback.answer("Bu hududda hozircha ma'lumot yo'q, boshqasini tanlang.", show_alert=True)
        return
    await state.set_state(RoyxatState.shahar)
    await callback.message.edit_text("Shahringizni tanlang:", reply_markup=shahar_klaviaturasi(shaharlar))
    await callback.answer()


@router.callback_query(RoyxatState.shahar, F.data.startswith("shahar:"))
async def shahar_tanlandi(callback: CallbackQuery, state: FSMContext) -> None:
    shahar_id = int(callback.data.split(":", 1)[1])
    malumot = await state.get_data()
    await royxatga_ol(callback.from_user.id, malumot["maqsad"], shahar_id)
    await state.clear()

    shahar = await bittasi(shahar_id)
    await callback.message.edit_text(
        f"✓ Ro'yxatdan o'tdingiz — shahar: {shahar.nom if shahar else '—'}.\n\n"
        "Bugungi namoz vaqtlari uchun /vaqt yuboring.\n\n"
        f"{MANBA_MATNI}"
    )
    await callback.answer()
