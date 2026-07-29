from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

NAMOZ_NOMLARI = ["bomdod", "peshin", "asr", "shom", "xufton"]
NAMOZ_KORSATISH = {
    "bomdod": "Bomdod", "peshin": "Peshin", "asr": "Asr", "shom": "Shom", "xufton": "Xufton",
}
DAQIQA_VARIANTLARI = [5, 10, 15, 20, 30]


def eslatma_menyu_klaviaturasi(yoqilgan: bool) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    holat = "🔕 O'chirish" if yoqilgan else "🔔 Yoqish"
    b.button(text=holat, callback_data="esl_yoq")
    b.button(text="🕌 Namozlarni tanlash", callback_data="esl_namoz_menyu")
    b.button(text="⏱ Necha daqiqa oldin", callback_data="esl_daq_menyu")
    b.adjust(1)
    return b.as_markup()


def eslatma_namozlar_klaviaturasi(tanlangan: set[str]) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    for nom in NAMOZ_NOMLARI:
        belgi = "✅" if nom in tanlangan else "⬜️"
        b.button(text=f"{belgi} {NAMOZ_KORSATISH[nom]}", callback_data=f"esl_namoz:{nom}")
    b.button(text="« Orqaga", callback_data="esl_orqaga")
    b.adjust(1)
    return b.as_markup()


def eslatma_daqiqa_klaviaturasi() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    for daq in DAQIQA_VARIANTLARI:
        b.button(text=f"{daq} daqiqa", callback_data=f"esl_daq:{daq}")
    b.button(text="« Orqaga", callback_data="esl_orqaga")
    b.adjust(3)
    return b.as_markup()
