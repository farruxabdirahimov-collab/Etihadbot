from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, WebAppInfo

from bot import miniapp_url
from bot.services.foydalanuvchi_xizmat import olish
from bot.services.shahar_xizmat import bittasi

router = Router()

BOT_NOMI = "Etihat — E'tiqod"

MANBA_MATNI = (
    "Namoz vaqtlari manbasi: namozvaqti.uz — "
    "«Book Media Nashr» taqvim kitobi asosida"
)


def _ilova_klaviaturasi() -> InlineKeyboardMarkup | None:
    manzil = miniapp_url.ol()
    if not manzil:
        return None
    tugma = InlineKeyboardButton(text="📱 Ilovani ochish", web_app=WebAppInfo(url=manzil))
    return InlineKeyboardMarkup(inline_keyboard=[[tugma]])


@router.message(CommandStart())
async def handle_start(message: Message) -> None:
    mavjud = await olish(message.from_user.id)
    shahar = await bittasi(mavjud.shahar_id) if mavjud and mavjud.shahar_id else None

    if shahar:
        matn = (
            "✅ <b>Assalomu alaykum!</b>\n\n"
            f"📍 Shahringiz: <b>{shahar.nom}</b>\n\n"
            "━━━━━━━━━━━━━━\n\n"
            "📱 Ilovada: namoz vaqtlari, qibla, qisqa suralar va sozlamalar\n\n"
            "🕌 /vaqt — bugungi vaqtlar\n"
            "🧭 /qibla — qibla yo'nalishi\n"
            "🔔 /bildirishnoma — eslatmalar\n\n"
            f"<i>{MANBA_MATNI}</i>"
        )
    else:
        matn = (
            "🌙 <b>Assalomu alaykum va rohmatulloh!</b>\n\n"
            f"Namoz va uning vaqtlari haqidagi «<b>{BOT_NOMI}</b>» ilovasiga "
            "xush kelibsiz.\n\n"
            "━━━━━━━━━━━━━━\n\n"
            "Boshlash uchun quyidagi tugmani bosing — ilovada shahringizni "
            "tanlaysiz va namoz vaqtlarini darhol ko'rasiz.\n\n"
            "Ilovada: namoz vaqtlari, qibla yo'nalishi, qisqa suralar, "
            "namoz tartibi va eslatma sozlamalari.\n\n"
            f"<i>{MANBA_MATNI}</i>"
        )

    klaviatura = _ilova_klaviaturasi()
    if klaviatura is None:
        matn += "\n\n⚠️ Ilova hozircha sozlanmagan. /vaqt buyrug'idan foydalaning."
    await message.answer(matn, reply_markup=klaviatura)
