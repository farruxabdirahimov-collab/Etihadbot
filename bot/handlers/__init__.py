from aiogram import Router

from bot.handlers.admin import router as admin_router
from bot.handlers.bildirishnoma import router as bildirishnoma_router
from bot.handlers.qibla import router as qibla_router
from bot.handlers.sozlama import router as sozlama_router
from bot.handlers.start import router as start_router
from bot.handlers.ulashish import router as ulashish_router
from bot.handlers.vaqt import router as vaqt_router

main_router = Router()
main_router.include_router(start_router)
main_router.include_router(vaqt_router)
main_router.include_router(qibla_router)
main_router.include_router(sozlama_router)
main_router.include_router(bildirishnoma_router)
main_router.include_router(ulashish_router)
main_router.include_router(admin_router)
