from fastapi import Header, HTTPException

from backend.auth import foydalanuvchini_tekshir
from bot.config import settings


async def joriy_foydalanuvchi(x_telegram_init_data: str = Header(...)) -> dict:
    """Telegram autentifikatsiyasini majburiy talab qiladi."""
    user = foydalanuvchini_tekshir(x_telegram_init_data, settings.bot_token)
    if user is None:
        raise HTTPException(status_code=401, detail="Yaroqsiz Telegram autentifikatsiyasi")
    return user


async def joriy_foydalanuvchi_ixtiyoriy(
    x_telegram_init_data: str | None = Header(None),
) -> dict | None:
    """Telegram tashqarisida — oddiy brauzerda yoki bosh ekranga qo'shilgan
    PWA'da — ochilganda None qaytaradi. Shunda ilova mehmon rejimida
    ishlaydi: sozlamalar qurilmaning o'zida saqlanadi, bildirishnoma esa
    faqat Telegram orqali beriladi."""
    if not x_telegram_init_data:
        return None
    return foydalanuvchini_tekshir(x_telegram_init_data, settings.bot_token)
