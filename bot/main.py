import asyncio
import logging

import uvicorn
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from backend.main import app as fastapi_app
from bot.config import settings
from bot.db.connection import engine
from bot.db.migratsiya import yangila
from bot.db.models import Base
from bot.handlers import main_router
from bot.scheduler import ishga_tushir


async def main() -> None:
    logging.basicConfig(level=logging.INFO)

    # scraper faqat shaharlar/namoz_vaqtlari/suralar jadvallarini yaratadi —
    # bot o'ziga xos jadvallarni (masalan foydalanuvchilar) shu yerda qo'shadi.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await yangila(engine)

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.include_router(main_router)

    scheduler = await ishga_tushir(bot)

    # Bot (polling) va Mini App backend (HTTP) bitta Railway servisida,
    # bitta protsessda birga ishlaydi — alohida servis kerak emas.
    server = uvicorn.Server(
        uvicorn.Config(fastapi_app, host="0.0.0.0", port=settings.port, log_level="info")
    )

    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await asyncio.gather(dp.start_polling(bot), server.serve())
    finally:
        scheduler.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
