from fastapi import Header, HTTPException

from backend.auth import foydalanuvchini_tekshir
from bot.config import settings


async def joriy_foydalanuvchi(x_telegram_init_data: str = Header(...)) -> dict:
    user = foydalanuvchini_tekshir(x_telegram_init_data, settings.bot_token)
    if user is None:
        raise HTTPException(status_code=401, detail="Yaroqsiz Telegram autentifikatsiyasi")
    return user
