"""
═══════════════════════════════════════════════════════════════
  MANBA YIG'ISH — namoz vaqtlari va qisqa suralar
═══════════════════════════════════════════════════════════════

  MANBA VA HUQUQ
  --------------
  Namoz vaqtlari namozvaqti.uz saytidan olinadi. Sayt shartiga ko'ra
  ma'lumot olinganda manba ko'rsatilishi SHART. Ilovaning har bir
  ekranida quyidagi yozuv bo'lishi kerak:

      "Namoz vaqtlari manbasi: namozvaqti.uz —
       «Book Media Nashr» taqvim kitobi asosida"

  Ommaviy ishga tushirishdan OLDIN sayt egalaridan yozma ruxsat
  olish tavsiya etiladi: t.me/namozvaqtiuz_bot

  Skript saytga hurmat bilan murojaat qiladi: so'rovlar orasida
  pauza bor va yiliga bir marta ishlatiladi.

  ISHLATISH
  ---------
      pip install -r requirements.txt
      export DATABASE_URL=postgresql://...
      python -m scraper.manba_yigish vaqtlar --yil 2026
      python -m scraper.manba_yigish suralar
"""

import argparse
import asyncio
import os
import sys
from datetime import date
from pathlib import Path

from scraper.sozlamalar import XORAZM, YIRIK_SHAHARLAR
from scraper.suralar import suralarni_yukla
from scraper.vaqtlar import vaqtlarni_yig


def main() -> None:
    p = argparse.ArgumentParser(description="Namoz ilovasi uchun manba yig'ish")
    p.add_argument("buyruq", choices=["vaqtlar", "suralar"])
    p.add_argument("--yil", type=int, default=date.today().year)
    p.add_argument("--dsn", default=None, help="PostgreSQL DSN")
    p.add_argument("--toplam", choices=["xorazm", "yirik", "hammasi"], default="xorazm")
    p.add_argument("--chiqish", default="suralar.json")
    a = p.parse_args()

    dsn = a.dsn or os.environ.get("DATABASE_URL")
    if not dsn:
        sys.exit("DATABASE_URL ko'rsatilmagan")

    if a.buyruq == "vaqtlar":
        shaharlar = {
            "xorazm": XORAZM,
            "yirik": YIRIK_SHAHARLAR,
            "hammasi": XORAZM + YIRIK_SHAHARLAR,
        }[a.toplam]
        asyncio.run(vaqtlarni_yig(dsn, a.yil, shaharlar))
    else:
        asyncio.run(suralarni_yukla(dsn, Path(a.chiqish)))


if __name__ == "__main__":
    main()
