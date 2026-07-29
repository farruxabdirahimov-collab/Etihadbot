from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

# Base.metadata.create_all faqat yangi jadval yaratadi, mavjud jadvalga
# ustun qo'shmaydi. Shuning uchun har bosqichda qo'shilgan yangi
# ustunlar shu yerda ALTER TABLE ... IF NOT EXISTS orqali qo'shiladi.
_ALTERLAR = [
    "ALTER TABLE foydalanuvchilar ADD COLUMN IF NOT EXISTS eslatma_yoqilgan BOOLEAN NOT NULL DEFAULT TRUE",
    "ALTER TABLE foydalanuvchilar ADD COLUMN IF NOT EXISTS eslatma_namozlar TEXT NOT NULL DEFAULT 'bomdod'",
    "ALTER TABLE foydalanuvchilar ADD COLUMN IF NOT EXISTS eslatma_daqiqa SMALLINT NOT NULL DEFAULT 10",
    "ALTER TABLE foydalanuvchilar ADD COLUMN IF NOT EXISTS eslatma_tugash_yoqilgan BOOLEAN NOT NULL DEFAULT FALSE",
    "ALTER TABLE foydalanuvchilar ADD COLUMN IF NOT EXISTS eslatma_tugash_daqiqa SMALLINT NOT NULL DEFAULT 15",
]


async def yangila(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        for buyruq in _ALTERLAR:
            await conn.execute(text(buyruq))
