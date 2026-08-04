from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault

from bot.config import settings

# Telegram'da «/» bosilganda ko'rinadigan ro'yxat. Admin buyruqlari
# bu yerda yo'q — ular faqat ADMIN_ID uchun alohida qo'shiladi.
OMMAVIY = [
    BotCommand(command="vaqt", description="Bugungi namoz vaqtlari"),
    BotCommand(command="qibla", description="Qibla yo'nalishi"),
    BotCommand(command="bildirishnoma", description="Eslatmalarni sozlash"),
    BotCommand(command="sozlama", description="Shaharni o'zgartirish"),
    BotCommand(command="ulashish", description="Do'stlarga tavsiya qilish"),
    BotCommand(command="start", description="Boshidan boshlash"),
]

ADMIN = OMMAVIY + [
    BotCommand(command="tekshir", description="Baza holati"),
    BotCommand(command="yigish_vaqtlar", description="Vaqtlarni yig'ish"),
    BotCommand(command="yigish_shahar", description="Bitta shaharni yig'ish"),
    BotCommand(command="yigish_suralar", description="Suralarni yuklash"),
    BotCommand(command="qaytadan", description="Ro'yxatni o'chirish (sinov)"),
]


async def ornat(bot: Bot) -> None:
    await bot.set_my_commands(OMMAVIY, scope=BotCommandScopeDefault())
    if settings.admin_id:
        await bot.set_my_commands(ADMIN, scope=BotCommandScopeChat(chat_id=settings.admin_id))
