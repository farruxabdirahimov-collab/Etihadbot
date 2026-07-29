from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from bot.config import settings
from bot.services.eslatma_xizmat import bugungi_eslatmalarni_reja, scheduler_ni_ornat


async def ishga_tushir(bot: Bot) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone=settings.timezone)
    scheduler_ni_ornat(scheduler)

    scheduler.add_job(
        bugungi_eslatmalarni_reja,
        CronTrigger(hour=0, minute=5, timezone=settings.timezone),
        args=[bot],
        id="kunlik_reja",
        replace_existing=True,
    )
    scheduler.start()

    # Bot istalgan vaqtda qayta ishga tushishi mumkin — shu kuni qolgan
    # eslatmalarni ham darhol rejalashtiramiz.
    await bugungi_eslatmalarni_reja(bot)

    return scheduler
