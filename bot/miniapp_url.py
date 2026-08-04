import re
from pathlib import Path

from bot.config import settings

_INDEX = Path(__file__).resolve().parent.parent / "miniapp" / "dist" / "index.html"


def _versiya() -> str:
    """Vite build'idagi JS fayl hash'i (masalan «Bi_LSO8c»).

    Frontend o'zgarganda hash ham o'zgaradi. Shu hash Mini App URL'iga
    qo'shilgani uchun Telegram WebView uni butunlay yangi manzil deb
    qabul qiladi va eski keshdan foydalana olmaydi."""
    if not _INDEX.exists():
        return ""
    moslik = re.search(r"index-([A-Za-z0-9_-]+)\.js", _INDEX.read_text(encoding="utf-8"))
    return moslik.group(1) if moslik else ""


VERSIYA = _versiya()


def ol() -> str:
    """Telegram tugmalariga qo'yiladigan Mini App manzili. MINIAPP_URL
    sozlanmagan bo'lsa bo'sh qator qaytaradi (tugma ko'rsatilmaydi)."""
    if not settings.miniapp_url:
        return ""
    if not VERSIYA:
        return settings.miniapp_url

    manzil = settings.miniapp_url
    # «https://domen.uz» ko'rinishida bo'lsa yo'l qismini qo'shamiz —
    # «https://domen.uz/?v=...» toza bo'ladi.
    if "?" not in manzil and not manzil.rstrip("/").rpartition("//")[2].count("/"):
        manzil = manzil.rstrip("/") + "/"

    ajratgich = "&" if "?" in manzil else "?"
    return f"{manzil}{ajratgich}v={VERSIYA}"
