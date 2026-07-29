from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.keyboards import MAQSADLAR, maqsad_klaviaturasi, shahar_klaviaturasi, viloyat_klaviaturasi
from bot.services.foydalanuvchi_xizmat import olish, royxatga_ol
from bot.services.shahar_xizmat import bittasi, sluglar_boyicha
from bot.states import RoyxatState
from bot.viloyatlar import VILOYAT_TARTIBI, VILOYATLAR

router = Router()

BOT_NOMI = "Etihat — E'tiqod"

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
        f"Assalomu alaykum va rohmatulloh!\n\n"
        f"Namoz va uning vaqtlari haqidagi «{BOT_NOMI}» ilovasiga xush kelibsiz. 🌙\n\n"
        "Sizga qulayroq bo'lishi uchun avval bitta savol: bizdan asosan nimani kutasiz?",
        reply_markup=maqsad_klaviaturasi(),
    )


@router.callback_query(RoyxatState.maqsad, F.data.startswith("maqsad:"))
async def maqsad_tanlandi(callback: CallbackQuery, state: FSMContext) -> None:
    maqsad = callback.data.split(":", 1)[1]
    await state.update_data(maqsad=maqsad)
    await state.set_state(RoyxatState.viloyat)
    await callback.message.edit_text(
        f"✓ Tanlandi: {MAQSADLAR[maqsad]}\n\nEndi qaysi viloyatdasiz?",
        reply_markup=viloyat_klaviaturasi(),
    )
    await callback.answer()


@router.callback_query(RoyxatState.viloyat, F.data.startswith("viloyat:"))
async def viloyat_tanlandi(callback: CallbackQuery, state: FSMContext) -> None:
    idx = int(callback.data.split(":", 1)[1])
    viloyat_nomi = VILOYAT_TARTIBI[idx]
    sluglar = VILOYATLAR[viloyat_nomi]
    shaharlar = await sluglar_boyicha(sluglar)

    if not shaharlar:
        await callback.answer("Bu viloyatda hozircha ma'lumot yo'q, boshqasini tanlang.", show_alert=True)
        return

    if len(shaharlar) == 1:
        # Bitta shahar bo'lsa, qo'shimcha qadamsiz to'g'ridan-to'g'ri ro'yxatdan o'tkazamiz.
        await _royxatni_yakunla(callback, state, shaharlar[0].id)
        return

    await state.update_data(viloyat=viloyat_nomi)
    await state.set_state(RoyxatState.shahar)
    await callback.message.edit_text(
        f"{viloyat_nomi} — aniq shahringizni tanlang:",
        reply_markup=shahar_klaviaturasi(shaharlar),
    )
    await callback.answer()


@router.callback_query(RoyxatState.shahar, F.data.startswith("shahar:"))
async def shahar_tanlandi(callback: CallbackQuery, state: FSMContext) -> None:
    shahar_id = int(callback.data.split(":", 1)[1])
    await _royxatni_yakunla(callback, state, shahar_id)


async def _royxatni_yakunla(callback: CallbackQuery, state: FSMContext, shahar_id: int) -> None:
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
