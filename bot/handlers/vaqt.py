from aiogram import Router
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, WebAppInfo

from bot import miniapp_url
from bot.services.foydalanuvchi_xizmat import olish
from bot.services.shahar_xizmat import bittasi
from bot.services.vaqt_xizmat import NOM_KORSATISH, joriy_holat

router = Router()


def _ilova_klaviaturasi() -> InlineKeyboardMarkup | None:
    manzil = miniapp_url.ol()
    if not manzil:
        return None
    tugma = InlineKeyboardButton(text="📱 Ilovani ochish", web_app=WebAppInfo(url=manzil))
    return InlineKeyboardMarkup(inline_keyboard=[[tugma]])


def _qolgan_matni(qolgan) -> str:
    if qolgan is None:
        return ""
    jami_daqiqa = int(qolgan.total_seconds() // 60)
    soat, daqiqa = divmod(jami_daqiqa, 60)
    if soat:
        return f"{soat} soat {daqiqa} daqiqa"
    return f"{daqiqa} daqiqa"


@router.message(Command("vaqt"))
async def vaqt_korsat(message: Message) -> None:
    foydalanuvchi = await olish(message.from_user.id)
    if not foydalanuvchi or not foydalanuvchi.shahar_id:
        await message.answer("Avval shahringizni tanlang: /start")
        return

    shahar = await bittasi(foydalanuvchi.shahar_id)
    holat = await joriy_holat(foydalanuvchi.shahar_id)
    if not holat["topildi"]:
        await message.answer("Kechirasiz, bugungi kun uchun ma'lumot topilmadi.")
        return

    bugun = holat["bugun"]
    qatorlar = [
        f"🕌 <b>{shahar.nom if shahar else ''}</b> — bugungi namoz vaqtlari\n",
        f"🌅 Bomdod: <b>{bugun.bomdod.strftime('%H:%M')}</b>",
        f"☀️ Quyosh: <b>{bugun.quyosh.strftime('%H:%M')}</b>",
        f"🌤 Peshin: <b>{bugun.peshin.strftime('%H:%M')}</b>",
        f"🌇 Asr: <b>{bugun.asr.strftime('%H:%M')}</b>",
        f"🌆 Shom: <b>{bugun.shom.strftime('%H:%M')}</b>",
        f"🌙 Xufton: <b>{bugun.xufton.strftime('%H:%M')}</b>",
    ]
    chegara = NOM_KORSATISH[holat["chegara_nom"]]
    qatorlar.append("")
    if holat["joriy_nom"]:
        joriy = NOM_KORSATISH[holat["joriy_nom"]]
        qatorlar.append(
            f"🕐 <b>{joriy}</b> vaqti kirdi — <b>{chegara}</b>gacha "
            f"<b>{_qolgan_matni(holat['qolgan'])}</b> bor"
        )
    elif holat["qolgan"] is not None:
        qatorlar.append(f"⏳ <b>{chegara}</b> namozigacha: <b>{_qolgan_matni(holat['qolgan'])}</b>")

    qatorlar.append("")
    qatorlar.append(
        "<i>Namoz vaqtlari manbasi: namozvaqti.uz — «Book Media Nashr» taqvim kitobi asosida</i>"
    )
    await message.answer("\n".join(qatorlar), reply_markup=_ilova_klaviaturasi())
