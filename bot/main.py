import asyncio
import logging

import uvicorn
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import MenuButtonWebApp, WebAppInfo

from backend.main import app as fastapi_app
from bot import buyruqlar, miniapp_url
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

    # Mini App backend'i (bir xil protsessda) eslatmalarni darhol qayta
    # rejalashtirish uchun shu bot obyektidan foydalanadi.
    fastapi_app.state.bot = bot

    # Ulashish havolasi uchun bot foydalanuvchi nomi — qo'lda sozlash
    # shart bo'lmasligi uchun Telegram'ning o'zidan olinadi.
    men = await bot.get_me()
    fastapi_app.state.bot_username = men.username or ""

    # «/» bosilganda chiqadigan buyruqlar ro'yxati.
    await buyruqlar.ornat(bot)

    scheduler = await ishga_tushir(bot)

    # MINIAPP_URL hali sozlanmagan bo'lsa (Railway domeni yaratilmagan),
    # tugma ko'rsatilmaydi — sinib qolgan havola bilan chalg'itmaslik uchun.
    ilova_manzili = miniapp_url.ol()
    if ilova_manzili:
        await bot.set_chat_menu_button(
            menu_button=MenuButtonWebApp(text="Ilova", web_app=WebAppInfo(url=ilova_manzili))
        )
        logging.info("Mini App manzili: %s", ilova_manzili)

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
