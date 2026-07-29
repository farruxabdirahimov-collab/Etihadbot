from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.db.models import Shahar

MAQSADLAR = {
    "organish": "📚 Faqat o'rganish",
    "vaqt_organish": "🕌 Vaqt + o'rganish",
    "vaqt": "⏰ Faqat vaqt",
    "erkin": "🔍 Erkin ko'rish",
}


def maqsad_klaviaturasi() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    for kalit, nom in MAQSADLAR.items():
        b.button(text=nom, callback_data=f"maqsad:{kalit}")
    b.adjust(1)
    return b.as_markup()


def hudud_klaviaturasi(prefix: str = "hudud") -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text="Xorazm shaharlari", callback_data=f"{prefix}:xorazm")
    b.button(text="Yirik shaharlar", callback_data=f"{prefix}:yirik")
    b.adjust(1)
    return b.as_markup()


def shahar_klaviaturasi(shaharlar: list[Shahar], prefix: str = "shahar") -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    for sh in shaharlar:
        b.button(text=sh.nom, callback_data=f"{prefix}:{sh.id}")
    b.adjust(2)
    return b.as_markup()
