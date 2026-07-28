from aiogram import Router

from bot.handlers.admin import router as admin_router
from bot.handlers.start import router as start_router

main_router = Router()
main_router.include_router(start_router)
main_router.include_router(admin_router)
