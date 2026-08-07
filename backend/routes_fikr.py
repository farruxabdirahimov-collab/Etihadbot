import html
import time

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field

from backend.dependencies import joriy_foydalanuvchi_ixtiyoriy
from bot.config import settings
from bot.services.foydalanuvchi_xizmat import olish
from bot.services.shahar_xizmat import bittasi

router = APIRouter(prefix="/api")

MATN_CHEGARASI = 1000
# Bir foydalanuvchi shuncha soniyada bir marta yubora oladi — tasodifiy
# ikki marta bosish va oddiy spamdan himoya.
KUTISH_SONIYA = 60

_oxirgi_yuborish: dict[int | str, float] = {}


class FikrTana(BaseModel):
    matn: str = Field(min_length=3, max_length=MATN_CHEGARASI)


@router.post("/fikr")
async def fikr_yubor(
    body: FikrTana, so_rov: Request, tg_user: dict | None = Depends(joriy_foydalanuvchi_ixtiyoriy)
) -> dict:
    # Telegram tashqarisidan (sayt/PWA) kelgan fikrni IP bo'yicha ajratamiz —
    # telegram_id yo'q, lekin spam himoyasi baribir kerak.
    kalit = tg_user["id"] if tg_user else f"ip:{so_rov.client.host if so_rov.client else 'nomalum'}"

    hozir = time.monotonic()
    oxirgi = _oxirgi_yuborish.get(kalit)
    if oxirgi is not None and hozir - oxirgi < KUTISH_SONIYA:
        qolgan = int(KUTISH_SONIYA - (hozir - oxirgi))
        raise HTTPException(status_code=429, detail=f"Iltimos, {qolgan} soniyadan keyin urinib ko'ring.")

    bot = getattr(so_rov.app.state, "bot", None)
    if bot is None or not settings.admin_id:
        raise HTTPException(status_code=503, detail="Fikr yuborish hozir mavjud emas.")

    if tg_user is not None:
        foydalanuvchi = await olish(tg_user["id"])
        shahar = await bittasi(foydalanuvchi.shahar_id) if foydalanuvchi and foydalanuvchi.shahar_id else None
        # Bot HTML parse_mode bilan ishlaydi — foydalanuvchi matni albatta
        # ekranlanadi, aks holda xabar buzilishi mumkin.
        ism = html.escape(tg_user.get("first_name") or "Noma'lum")
        username = tg_user.get("username")
        kim = f"@{html.escape(username)}" if username else f"ID {tg_user['id']}"
        sarlavha = f"👤 {ism} ({kim})\n📍 {html.escape(shahar.nom) if shahar else '—'}"
    else:
        sarlavha = "👤 Mehmon (sayt orqali)"

    xabar = (
        "💬 <b>Yangi fikr-mulohaza</b>\n\n"
        f"{sarlavha}\n\n"
        f"{html.escape(body.matn.strip())}"
    )
    await bot.send_message(settings.admin_id, xabar)

    _oxirgi_yuborish[kalit] = hozir
    return {"yuborildi": True}
