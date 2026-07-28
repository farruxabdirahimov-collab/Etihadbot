# Bu sxema bot/db/models.py dagi SQLAlchemy modellari bilan bir xil
# bo'lishi shart — ustun nomlari va turlari mos kelmasa, scraper yozgan
# qatorlarni ORM o'qiy olmaydi. Sxema o'zgarsa, ikkalasini ham yangilang.

SXEMA = """
CREATE TABLE IF NOT EXISTS shaharlar (
    id          SERIAL PRIMARY KEY,
    slug        TEXT UNIQUE NOT NULL,
    nom         TEXT NOT NULL,
    viloyat     TEXT,
    lat         DOUBLE PRECISION,
    lon         DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS namoz_vaqtlari (
    id          BIGSERIAL PRIMARY KEY,
    shahar_id   INTEGER NOT NULL REFERENCES shaharlar(id) ON DELETE CASCADE,
    sana        DATE NOT NULL,
    bomdod      TIME NOT NULL,
    quyosh      TIME NOT NULL,
    peshin      TIME NOT NULL,
    asr         TIME NOT NULL,
    shom        TIME NOT NULL,
    xufton      TIME NOT NULL,
    qamar_kuni  SMALLINT,
    manba       TEXT NOT NULL DEFAULT 'namozvaqti.uz',
    olingan     TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (shahar_id, sana)
);

CREATE INDEX IF NOT EXISTS ix_vaqt_shahar_sana
    ON namoz_vaqtlari (shahar_id, sana);

CREATE TABLE IF NOT EXISTS suralar (
    raqam       SMALLINT PRIMARY KEY,
    nom_uz      TEXT NOT NULL,
    nom_ar      TEXT NOT NULL,
    oyat_soni   SMALLINT NOT NULL,
    daraja      TEXT NOT NULL,          -- boshlangich | orta | murakkab
    maqom       TEXT,                   -- makka | madina
    matn        JSONB,                  -- [{oyat, arab, talaffuz}]
    manba       TEXT,
    tasdiqlangan BOOLEAN NOT NULL DEFAULT FALSE
);
"""


async def baza_tayyorla(pool):
    async with pool.acquire() as c:
        await c.execute(SXEMA)
    print("✓ Sxema tayyor")
