import asyncio
import json
from pathlib import Path

import httpx

from scraper.sxema import baza_tayyorla

# Qur'on matni tasdiqlangan manbadan olinadi — qo'lda yozilmaydi.
# alquran.cloud Usmoniy mushaf matnini beradi.
#
# MUHIM: yuklab olingandan so'ng matnni bosma mushaf bilan
# solishtirib chiqish shart. `tasdiqlangan` ustuni shuning uchun.

SURA_ROYXATI = [
    # (raqam, nom_uz, nom_ar, oyat, daraja)
    (112, "Ixlos",    "الإخلاص",  4,  "boshlangich"),
    (113, "Falaq",    "الفلق",    5,  "boshlangich"),
    (114, "Nas",      "الناس",    6,  "boshlangich"),
    (108, "Kavsar",   "الكوثر",   3,  "boshlangich"),
    (103, "Asr",      "العصر",    3,  "boshlangich"),
    (110, "Nasr",     "النصر",    3,  "boshlangich"),
    (106, "Quraysh",  "قريش",     4,  "boshlangich"),
    (111, "Masad",    "المسد",    5,  "boshlangich"),

    (105, "Fil",      "الفيل",    5,  "orta"),
    (109, "Kofirun",  "الكافرون", 6,  "orta"),
    (107, "Mo'un",    "الماعون",  7,  "orta"),
    (97,  "Qadr",     "القدر",    5,  "orta"),
    (102, "Takosur",  "التكاثر",  8,  "orta"),
    (104, "Humaza",   "الهمزة",   9,  "orta"),
    (99,  "Zalzala",  "الزلزلة",  8,  "orta"),

    (101, "Qori'a",   "القارعة",  11, "murakkab"),
    (100, "Odiyot",   "العاديات", 11, "murakkab"),
    (95,  "Tiyn",     "التين",    8,  "murakkab"),
    (94,  "Sharh",    "الشرح",    8,  "murakkab"),
    (93,  "Zuho",     "الضحى",    11, "murakkab"),

    (1,   "Fotiha",   "الفاتحة",  7,  "asosiy"),   # har rakatda o'qiladi
]

QURON_API = "https://api.alquran.cloud/v1/surah/{n}/quran-uthmani"


async def suralarni_yukla(dsn: str, chiqish: Path):
    import asyncpg

    pool = await asyncpg.create_pool(dsn, min_size=1, max_size=2)
    await baza_tayyorla(pool)

    yigilgan = []
    async with httpx.AsyncClient(timeout=30) as mijoz:
        for raqam, nom_uz, nom_ar, oyat, daraja in SURA_ROYXATI:
            try:
                javob = await mijoz.get(QURON_API.format(n=raqam))
                javob.raise_for_status()
                malumot = javob.json()["data"]
            except Exception as x:
                print(f"  ✗ {nom_uz}: {x}")
                continue

            oyatlar = [
                {"oyat": a["numberInSurah"], "arab": a["text"]}
                for a in malumot["ayahs"]
            ]

            if len(oyatlar) != oyat:
                print(f"  ⚠ {nom_uz}: kutilgan {oyat}, kelgan {len(oyatlar)}")

            yozuv = {
                "raqam": raqam,
                "nom_uz": nom_uz,
                "nom_ar": nom_ar,
                "oyat_soni": len(oyatlar),
                "daraja": daraja,
                "maqom": malumot.get("revelationType", "").lower(),
                "matn": oyatlar,
            }
            yigilgan.append(yozuv)

            async with pool.acquire() as c:
                await c.execute(
                    """INSERT INTO suralar
                       (raqam, nom_uz, nom_ar, oyat_soni, daraja, maqom,
                        matn, manba, tasdiqlangan)
                       VALUES ($1,$2,$3,$4,$5,$6,$7::jsonb,$8,FALSE)
                       ON CONFLICT (raqam) DO UPDATE SET
                           matn = EXCLUDED.matn, manba = EXCLUDED.manba""",
                    raqam, nom_uz, nom_ar, len(oyatlar), daraja,
                    yozuv["maqom"], json.dumps(oyatlar, ensure_ascii=False),
                    "alquran.cloud / quran-uthmani",
                )

            print(f"  ✓ {nom_uz} — {len(oyatlar)} oyat")
            await asyncio.sleep(0.4)

    chiqish.write_text(
        json.dumps(yigilgan, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    await pool.close()

    print(f"\n═══ {len(yigilgan)} sura saqlandi → {chiqish} ═══")
    print("    DIQQAT: matnni bosma mushaf bilan solishtirib chiqing,")
    print("    so'ngra bazada tasdiqlangan = TRUE qilib belgilang.")
