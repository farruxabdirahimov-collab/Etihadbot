import hashlib
import hmac
import json
from urllib.parse import parse_qsl


def foydalanuvchini_tekshir(init_data: str, bot_token: str) -> dict | None:
    """Telegram WebApp initData imzosini tekshiradi (Telegram hujjatidagi
    rasmiy algoritm). Noto'g'ri yoki soxta bo'lsa None qaytaradi — TZ M- xavfsizlik talabi."""
    try:
        juftliklar = dict(parse_qsl(init_data, strict_parsing=True))
    except ValueError:
        return None

    qabul_qilingan_hash = juftliklar.pop("hash", None)
    if not qabul_qilingan_hash:
        return None

    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(juftliklar.items()))
    maxfiy_kalit = hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()
    hisoblangan_hash = hmac.new(maxfiy_kalit, data_check_string.encode(), hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hisoblangan_hash, qabul_qilingan_hash):
        return None

    user_json = juftliklar.get("user")
    return json.loads(user_json) if user_json else None
