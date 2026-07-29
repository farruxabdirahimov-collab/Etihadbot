from sqlalchemy import select

from bot.db.connection import async_session
from bot.db.models import Foydalanuvchi


async def olish(telegram_id: int) -> Foydalanuvchi | None:
    async with async_session() as s:
        natija = await s.execute(select(Foydalanuvchi).where(Foydalanuvchi.telegram_id == telegram_id))
        return natija.scalar_one_or_none()


async def royxatga_ol(telegram_id: int, maqsad: str, shahar_id: int) -> Foydalanuvchi:
    async with async_session() as s:
        mavjud = await s.scalar(select(Foydalanuvchi).where(Foydalanuvchi.telegram_id == telegram_id))
        if mavjud:
            mavjud.maqsad = maqsad
            mavjud.shahar_id = shahar_id
        else:
            mavjud = Foydalanuvchi(telegram_id=telegram_id, maqsad=maqsad, shahar_id=shahar_id)
            s.add(mavjud)
        await s.commit()
        await s.refresh(mavjud)
        return mavjud


async def shaharni_yangila(telegram_id: int, shahar_id: int) -> None:
    async with async_session() as s:
        foydalanuvchi = await s.scalar(select(Foydalanuvchi).where(Foydalanuvchi.telegram_id == telegram_id))
        if foydalanuvchi:
            foydalanuvchi.shahar_id = shahar_id
            await s.commit()


async def ochirish(telegram_id: int) -> bool:
    """Foydalanuvchi yozuvini o'chiradi — sinov uchun /start oqimini qaytadan boshlash imkonini beradi."""
    async with async_session() as s:
        foydalanuvchi = await s.scalar(select(Foydalanuvchi).where(Foydalanuvchi.telegram_id == telegram_id))
        if not foydalanuvchi:
            return False
        await s.delete(foydalanuvchi)
        await s.commit()
        return True
