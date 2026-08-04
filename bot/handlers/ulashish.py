from urllib.parse import quote

from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

router = Router()

TAVSIYA_MATNI = (
    "Namoz vaqtlari va namozni o'rganish uchun «Etihat — E'tiqod» botini tavsiya qilaman."
)


@router.message(Command("ulashish"))
async def ulashish(message: Message, bot: Bot) -> None:
    men = await bot.get_me()
    havola = f"https://t.me/{men.username}"
    share_url = f"https://t.me/share/url?url={quote(havola)}&text={quote(TAVSIYA_MATNI)}"

    tugma = InlineKeyboardButton(text="📤 Do'stlarga yuborish", url=share_url)
    await message.answer(
        "🤝 <b>Do'stlaringizga tavsiya qiling</b>\n\n"
        "Bir kishiga namoz vaqtini eslatish — sadaqai joriya.\n\n"
        f"Havola: {havola}",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[tugma]]),
    )
