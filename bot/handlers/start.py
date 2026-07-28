from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()

# Manba yozuvi barcha ekranlarda majburiy ko'rsatiladi (TZ 6-bo'lim).
MANBA_MATNI = (
    "Namoz vaqtlari manbasi: namozvaqti.uz — "
    "«Book Media Nashr» taqvim kitobi asosida"
)


@router.message(CommandStart())
async def handle_start(message: Message) -> None:
    await message.answer(
        "Assalomu alaykum! Bot ishga tushdi (0-bosqich smoke test).\n\n"
        f"{MANBA_MATNI}"
    )
