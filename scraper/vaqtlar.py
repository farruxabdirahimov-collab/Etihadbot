import asyncio
import re
from datetime import date, datetime, time

import httpx
from bs4 import BeautifulSoup

from scraper.sozlamalar import ASOS, MANBA_IZOHI, MANBA_NOMI, OYLAR, PAUZA, VAQT_RE
from scraper.sxema import baza_tayyorla


def oylik_jadval_ajrat(html: str):
    """Oylik sahifadan kunlik vaqtlarni ajratib oladi."""
    sup = BeautifulSoup(html, "lxml")
    natija = []

    jadval = None
    for t in sup.find_all("table"):
        sarlavha = t.get_text(" ", strip=True).lower()
        if "bomdod" in sarlavha and "xufton" in sarlavha:
            jadval = t
            break
    if jadval is None:
        return natija

    for qator in jadval.find_all("tr"):
        kataklar = [k.get_text(strip=True) for k in qator.find_all(["td", "th"])]
        if len(kataklar) < 7:
            continue

        # Birinchi katak: "1 Se", "12 Sha" ko'rinishida
        kun_moslik = re.match(r"^(\d{1,2})", kataklar[0])
        if not kun_moslik:
            continue

        vaqtlar = [k for k in kataklar[1:7]]
        if not all(VAQT_RE.match(v) for v in vaqtlar):
            continue

        qamar = None
        if len(kataklar) >= 8 and kataklar[7].isdigit():
            qamar = int(kataklar[7])

        natija.append({
            "kun": int(kun_moslik.group(1)),
            "bomdod": vaqtlar[0],
            "quyosh": vaqtlar[1],
            "peshin": vaqtlar[2],
            "asr": vaqtlar[3],
            "shom": vaqtlar[4],
            "xufton": vaqtlar[5],
            "qamar": qamar,
        })

    return natija


async def shahar_yili(mijoz: httpx.AsyncClient, slug: str, yil: int):
    """Bitta shahar uchun 12 oylik ma'lumotni yig'adi."""
    barchasi = []
    for oy in range(1, 13):
        url = f"{ASOS}/oylik/{oy}/{slug}"
        try:
            javob = await mijoz.get(url)
            javob.raise_for_status()
        except httpx.HTTPError as x:
            print(f"  ✗ {slug} {OYLAR[oy]}: {x}")
            await asyncio.sleep(PAUZA)
            continue

        kunlar = oylik_jadval_ajrat(javob.text)
        if not kunlar:
            print(f"  ⚠ {slug} {OYLAR[oy]}: jadval topilmadi")
        for k in kunlar:
            try:
                k["sana"] = date(yil, oy, k["kun"])
            except ValueError:
                continue      # 31-fevral kabi xatolar
            barchasi.append(k)

        print(f"  · {slug} {OYLAR[oy]}: {len(kunlar)} kun")
        await asyncio.sleep(PAUZA)

    return barchasi


async def shahar_yoz(pool, slug: str, nom: str):
    async with pool.acquire() as c:
        return await c.fetchval(
            """INSERT INTO shaharlar (slug, nom) VALUES ($1, $2)
               ON CONFLICT (slug) DO UPDATE SET nom = EXCLUDED.nom
               RETURNING id""",
            slug, nom,
        )


def _vaqt(hhmm: str) -> time:
    """'07:02' kabi satrni Python time obyektiga aylantiradi — asyncpg
    ::time ustuniga satr emas, aynan time obyektini kutadi."""
    return datetime.strptime(hhmm, "%H:%M").time()


async def vaqtlar_yoz(pool, shahar_id: int, kunlar: list):
    if not kunlar:
        return 0
    qatorlar = [
        (shahar_id, k["sana"], _vaqt(k["bomdod"]), _vaqt(k["quyosh"]), _vaqt(k["peshin"]),
         _vaqt(k["asr"]), _vaqt(k["shom"]), _vaqt(k["xufton"]), k["qamar"], MANBA_NOMI)
        for k in kunlar
    ]
    async with pool.acquire() as c:
        await c.executemany(
            """INSERT INTO namoz_vaqtlari
               (shahar_id, sana, bomdod, quyosh, peshin, asr, shom,
                xufton, qamar_kuni, manba)
               VALUES ($1,$2,$3::time,$4::time,$5::time,$6::time,
                       $7::time,$8::time,$9,$10)
               ON CONFLICT (shahar_id, sana) DO UPDATE SET
                   bomdod = EXCLUDED.bomdod, quyosh = EXCLUDED.quyosh,
                   peshin = EXCLUDED.peshin, asr    = EXCLUDED.asr,
                   shom   = EXCLUDED.shom,   xufton = EXCLUDED.xufton,
                   qamar_kuni = EXCLUDED.qamar_kuni,
                   olingan = now()""",
            qatorlar,
        )
    return len(qatorlar)


async def vaqtlarni_yig(dsn: str, yil: int, shaharlar: list):
    import asyncpg

    pool = await asyncpg.create_pool(dsn, min_size=1, max_size=4)
    await baza_tayyorla(pool)

    sarlavhalar = {
        "User-Agent": "NamozIlova/1.0 (hurmat bilan; bog'lanish: t.me/Drfarrukhmission)"
    }

    jami = 0
    async with httpx.AsyncClient(headers=sarlavhalar, timeout=30) as mijoz:
        for slug in shaharlar:
            print(f"\n▸ {slug}")
            kunlar = await shahar_yili(mijoz, slug, yil)
            shahar_id = await shahar_yoz(pool, slug, slug.capitalize())
            n = await vaqtlar_yoz(pool, shahar_id, kunlar)
            jami += n
            print(f"  ✓ {n} kun saqlandi")

    await pool.close()
    print(f"\n═══ Jami {jami} kun · manba: {MANBA_NOMI} ═══")
    print(f"    {MANBA_IZOHI}")
    return jami
