from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.services.foydalanuvchi_xizmat import olish
from bot.services.shahar_xizmat import bittasi
from bot.services.vaqt_xizmat import NOM_KORSATISH, joriy_holat

router = Router()


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
        f"{shahar.nom if shahar else ''} — bugungi namoz vaqtlari:",
        "",
        f"Bomdod: {bugun.bomdod.strftime('%H:%M')}",
        f"Quyosh: {bugun.quyosh.strftime('%H:%M')}",
        f"Peshin: {bugun.peshin.strftime('%H:%M')}",
        f"Asr:    {bugun.asr.strftime('%H:%M')}",
        f"Shom:   {bugun.shom.strftime('%H:%M')}",
        f"Xufton: {bugun.xufton.strftime('%H:%M')}",
    ]
    if holat["keyingi_nom"]:
        nom = NOM_KORSATISH[holat["keyingi_nom"]]
        qatorlar.append("")
        qatorlar.append(f"⏳ {nom} namozigacha: {_qolgan_matni(holat['qolgan'])}")

    qatorlar.append("")
    qatorlar.append(
        "Namoz vaqtlari manbasi: namozvaqti.uz — «Book Media Nashr» taqvim kitobi asosida"
    )
    await message.answer("\n".join(qatorlar))
