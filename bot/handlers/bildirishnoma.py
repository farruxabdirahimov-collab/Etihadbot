from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from bot.db.models import Foydalanuvchi
from bot.keyboards_eslatma import (
    NAMOZ_KORSATISH,
    eslatma_daqiqa_klaviaturasi,
    eslatma_menyu_klaviaturasi,
    eslatma_namozlar_klaviaturasi,
)
from bot.services.eslatma_xizmat import bitta_foydalanuvchi_uchun_reja
from bot.services.foydalanuvchi_xizmat import (
    eslatma_daqiqasini_belgila,
    eslatma_namozini_almashtir,
    eslatmani_almashtir,
    olish,
)

router = Router()


def _holat_matni(f: Foydalanuvchi) -> str:
    holat = "yoqilgan ✅" if f.eslatma_yoqilgan else "o'chirilgan ⛔️"
    if f.eslatma_namozlar:
        namozlar = ", ".join(NAMOZ_KORSATISH[n] for n in f.eslatma_namozlar.split(",") if n in NAMOZ_KORSATISH)
    else:
        namozlar = "tanlanmagan"
    return (
        f"🔔 Bildirishnoma: {holat}\n"
        f"🕌 Namozlar: {namozlar}\n"
        f"⏱ Necha daqiqa oldin: {f.eslatma_daqiqa} daqiqa"
    )


@router.message(Command("bildirishnoma"))
async def bildirishnoma_menyu(message: Message) -> None:
    foydalanuvchi = await olish(message.from_user.id)
    if not foydalanuvchi or not foydalanuvchi.shahar_id:
        await message.answer("Avval ro'yxatdan o'ting: /start")
        return
    await message.answer(
        _holat_matni(foydalanuvchi),
        reply_markup=eslatma_menyu_klaviaturasi(foydalanuvchi.eslatma_yoqilgan),
    )


@router.callback_query(F.data == "esl_yoq")
async def esl_yoq(callback: CallbackQuery, bot: Bot) -> None:
    yoqilgan = await eslatmani_almashtir(callback.from_user.id)
    if yoqilgan is None:
        await callback.answer("Avval ro'yxatdan o'ting: /start", show_alert=True)
        return
    await bitta_foydalanuvchi_uchun_reja(bot, callback.from_user.id)
    foydalanuvchi = await olish(callback.from_user.id)
    await callback.message.edit_text(
        _holat_matni(foydalanuvchi), reply_markup=eslatma_menyu_klaviaturasi(yoqilgan)
    )
    await callback.answer("Yoqildi" if yoqilgan else "O'chirildi")


@router.callback_query(F.data == "esl_namoz_menyu")
async def esl_namoz_menyu(callback: CallbackQuery) -> None:
    foydalanuvchi = await olish(callback.from_user.id)
    tanlangan = set(foydalanuvchi.eslatma_namozlar.split(",")) if foydalanuvchi.eslatma_namozlar else set()
    await callback.message.edit_text(
        "Qaysi namozlar uchun eslatma kerak? (bir nechtasini tanlashingiz mumkin)",
        reply_markup=eslatma_namozlar_klaviaturasi(tanlangan),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("esl_namoz:"))
async def esl_namoz_tanlash(callback: CallbackQuery, bot: Bot) -> None:
    nom = callback.data.split(":", 1)[1]
    yangi = await eslatma_namozini_almashtir(callback.from_user.id, nom)
    await bitta_foydalanuvchi_uchun_reja(bot, callback.from_user.id)
    tanlangan = set(yangi.split(",")) if yangi else set()
    await callback.message.edit_reply_markup(reply_markup=eslatma_namozlar_klaviaturasi(tanlangan))
    await callback.answer()


@router.callback_query(F.data == "esl_daq_menyu")
async def esl_daq_menyu(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        "Namozdan necha daqiqa oldin eslatilsin?", reply_markup=eslatma_daqiqa_klaviaturasi()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("esl_daq:"))
async def esl_daq_tanlash(callback: CallbackQuery, bot: Bot) -> None:
    daqiqa = int(callback.data.split(":", 1)[1])
    await eslatma_daqiqasini_belgila(callback.from_user.id, daqiqa)
    await bitta_foydalanuvchi_uchun_reja(bot, callback.from_user.id)
    foydalanuvchi = await olish(callback.from_user.id)
    await callback.message.edit_text(
        _holat_matni(foydalanuvchi),
        reply_markup=eslatma_menyu_klaviaturasi(foydalanuvchi.eslatma_yoqilgan),
    )
    await callback.answer(f"{daqiqa} daqiqa belgilandi")


@router.callback_query(F.data == "esl_orqaga")
async def esl_orqaga(callback: CallbackQuery) -> None:
    foydalanuvchi = await olish(callback.from_user.id)
    await callback.message.edit_text(
        _holat_matni(foydalanuvchi),
        reply_markup=eslatma_menyu_klaviaturasi(foydalanuvchi.eslatma_yoqilgan),
    )
    await callback.answer()
