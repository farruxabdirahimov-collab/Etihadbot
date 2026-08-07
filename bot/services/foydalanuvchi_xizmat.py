from sqlalchemy import select

from bot.db.connection import async_session
from bot.db.models import Foydalanuvchi


async def olish(telegram_id: int) -> Foydalanuvchi | None:
    async with async_session() as s:
        natija = await s.execute(select(Foydalanuvchi).where(Foydalanuvchi.telegram_id == telegram_id))
        return natija.scalar_one_or_none()


async def shaharni_yangila(telegram_id: int, shahar_id: int) -> None:
    async with async_session() as s:
        foydalanuvchi = await s.scalar(select(Foydalanuvchi).where(Foydalanuvchi.telegram_id == telegram_id))
        if foydalanuvchi:
            foydalanuvchi.shahar_id = shahar_id
            await s.commit()


async def ochirish(telegram_id: int) -> bool:
    """Foydalanuvchi yozuvini o'chiradi — sinov uchun /start oqimini qaytadan
    boshlash uchun, shuningdek botni bloklaganlarni avtomatik tozalash uchun."""
    async with async_session() as s:
        foydalanuvchi = await s.scalar(select(Foydalanuvchi).where(Foydalanuvchi.telegram_id == telegram_id))
        if not foydalanuvchi:
            return False
        await s.delete(foydalanuvchi)
        await s.commit()
        return True


async def eslatmani_almashtir(telegram_id: int) -> bool | None:
    """Bildirishnomani yoqadi/o'chiradi, yangi holatni qaytaradi."""
    async with async_session() as s:
        f = await s.scalar(select(Foydalanuvchi).where(Foydalanuvchi.telegram_id == telegram_id))
        if not f:
            return None
        f.eslatma_yoqilgan = not f.eslatma_yoqilgan
        await s.commit()
        return f.eslatma_yoqilgan


async def eslatma_namozini_almashtir(telegram_id: int, nom: str) -> str | None:
    """Berilgan namozni eslatma ro'yxatiga qo'shadi yoki olib tashlaydi."""
    async with async_session() as s:
        f = await s.scalar(select(Foydalanuvchi).where(Foydalanuvchi.telegram_id == telegram_id))
        if not f:
            return None
        tanlangan = [n for n in f.eslatma_namozlar.split(",") if n]
        if nom in tanlangan:
            tanlangan.remove(nom)
        else:
            tanlangan.append(nom)
        f.eslatma_namozlar = ",".join(tanlangan)
        await s.commit()
        return f.eslatma_namozlar


async def eslatma_daqiqasini_belgila(telegram_id: int, daqiqa: int) -> None:
    async with async_session() as s:
        f = await s.scalar(select(Foydalanuvchi).where(Foydalanuvchi.telegram_id == telegram_id))
        if f:
            f.eslatma_daqiqa = daqiqa
            await s.commit()


async def eslatma_tugashini_almashtir(telegram_id: int) -> bool | None:
    """Vaqt tugashidan oldingi ogohlantirishni yoqadi/o'chiradi."""
    async with async_session() as s:
        f = await s.scalar(select(Foydalanuvchi).where(Foydalanuvchi.telegram_id == telegram_id))
        if not f:
            return None
        f.eslatma_tugash_yoqilgan = not f.eslatma_tugash_yoqilgan
        await s.commit()
        return f.eslatma_tugash_yoqilgan


async def eslatma_tugash_daqiqasini_belgila(telegram_id: int, daqiqa: int) -> None:
    async with async_session() as s:
        f = await s.scalar(select(Foydalanuvchi).where(Foydalanuvchi.telegram_id == telegram_id))
        if f:
            f.eslatma_tugash_daqiqa = daqiqa
            await s.commit()
