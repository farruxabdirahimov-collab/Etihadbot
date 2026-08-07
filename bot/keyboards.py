from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.db.models import Shahar
from bot.viloyatlar import VILOYAT_TARTIBI


def viloyat_klaviaturasi(prefix: str = "viloyat") -> InlineKeyboardMarkup:
    """Barcha viloyatlarni teng huquqli, alifbo emas — bir xil formatda ko'rsatadi."""
    b = InlineKeyboardBuilder()
    for i, nom in enumerate(VILOYAT_TARTIBI):
        b.button(text=nom, callback_data=f"{prefix}:{i}")
    b.adjust(2)
    return b.as_markup()


def shahar_klaviaturasi(shaharlar: list[Shahar], prefix: str = "shahar") -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    for sh in shaharlar:
        b.button(text=sh.nom, callback_data=f"{prefix}:{sh.id}")
    b.adjust(2)
    return b.as_markup()
