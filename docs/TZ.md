# NAMOZ ILOVASI — TEXNIK TOPSHIRIQ VA BOSQICHLI REJA

**Versiya:** 1.0 · 28 iyul 2026
**Maqsad:** 4 hafta ichida to'liq ishlaydigan Telegram bot + Mini App
**Muallif:** Farrux Abdirahimov

---

## 1. MAHSULOT TA'RIFI

### 1.1 Muammo

Mavjud ilovalar (Islom UZ va boshqalar) og'ir interfeys, noaniq manba va faqat vaqt ko'rsatish bilan cheklangan. Foydalanuvchi namozni **o'rganishi** uchun alohida manba izlashga majbur.

### 1.2 Yechim

Uch narsani bitta joyda birlashtirgan ilova:

1. **Aniq vaqt** — rasmiy taqvim manbasidan, bir qarashda tushunarli
2. **O'rganish** — namoz tartibi, zam suralar, darajaga qarab o'sish
3. **Davomiylik** — qazo hisobi, Qur'on progressi, ro'za zanjiri

### 1.3 Asosiy farqlovchi xususiyat

**Svetofor tizimi.** Butun ekran qolgan vaqtga qarab rang o'zgartiradi: yashil (20+ daqiqa), sariq (10–20), qizil (0–10). Foydalanuvchi raqamni o'qimasdan, ekranga bir qarab holatni tushunadi.

---

## 2. MA'LUMOT MANBASI

### 2.1 Asosiy manba

**namozvaqti.uz** — 79 shahar, oylik jadval sahifalari (`/oylik/{oy}/{shahar}`).

| Ustun | Izoh |
|---|---|
| Kun | Sana + hafta kuni qisqartmasi |
| Bomdod, Quyosh, Peshin, Asr, Shom, Xufton | HH:MM |
| Qamar | Hijriy oy kuni |

**Huquqiy shart:** sayt qoidasiga ko'ra ma'lumot olinganda manba ko'rsatilishi shart. Har ekranda quyidagi yozuv bo'ladi:

> Namoz vaqtlari manbasi: namozvaqti.uz — «Book Media Nashr» taqvim kitobi asosida

### 2.2 Zaxira manba

**Aladhan API** (`api.aladhan.com`) — agar sayt tuzilishi o'zgarsa, yangi shahar kerak bo'lsa yoki ruxsat olinmasa.

### 2.3 Yig'ish rejimi

- Yiliga bir marta to'liq (12 so'rov × shahar soni)
- Oyiga bir marta keyingi oyni qayta tekshirish
- So'rovlar orasida 1.5 soniya pauza
- Bosqichma-bosqich: avval Xorazm (6 shahar), keyin yirik shaharlar

### 2.4 Qur'on matni

**alquran.cloud** — Usmoniy mushaf. Xotiradan yozilmaydi.
Yuklab olingandan so'ng bosma mushaf bilan solishtiriladi, keyin `tasdiqlangan = TRUE` qilinadi.

---

## 3. FUNKSIONAL TALABLAR

### 3.1 Bot (Telegram)

| Kod | Funksiya | Ustuvorlik |
|---|---|---|
| B-01 | `/start` — ro'yxatdan o'tish, shahar tanlash | Kritik |
| B-02 | Maqsad so'rovi (A: o'rganish / B: vaqt+o'rganish / C: vaqt / D: erkin) | Kritik |
| B-03 | `/vaqt` — bugungi 5 vaqt + keyingi namozgacha qolgan vaqt | Kritik |
| B-04 | Bildirishnoma sozlash (qaysi namoz, necha daqiqa oldin) | Kritik |
| B-05 | Uy manzili kiritish (qasr uchun) | Yuqori |
| B-06 | `/qazo` — qazo namoz hisoblagichi | O'rta |
| B-07 | «Ilovani ochish» tugmasi (Mini App) | Kritik |
| B-08 | `/sozlama` — til, shahar, bildirishnoma | Yuqori |

### 3.2 Mini App (interfeys)

| Kod | Funksiya | Ustuvorlik |
|---|---|---|
| M-01 | Jonli soat + teskari sanoq (MM:SS) | Kritik |
| M-02 | Svetofor rang tizimi | Kritik |
| M-03 | Halqa progress indikatori | Yuqori |
| M-04 | Rakat ko'rsatkichi (sunnat/farz ajratilgan) | Kritik |
| M-05 | «O'qidingizmi?» tasdiq mexanizmi | Yuqori |
| M-06 | Zam sura tavsiyasi (3 daraja) | Yuqori |
| M-07 | Qisqa suralar o'quvchi (20 ta, oflayn) | Yuqori |
| M-08 | «Qanday o'qiladi?» qoida oynasi | O'rta |
| M-09 | Qazo namozlar bo'limi | O'rta |
| M-10 | Qasr rejimi (70+ km, 7 kun qoidasi) | O'rta |
| M-11 | Qibla | Past |
| M-12 | Qur'on progress tracker | Past |

### 3.3 Rejimlar

| Kod | Rejim | Xususiyat |
|---|---|---|
| R-01 | Juma | Xutbagacha sanoq, masjid tanlash, Kahf surasi |
| R-02 | Ramazon | Saharlik/iftorlik sanoq, 30 kunlik zanjir, taroveh, oxirgi o'n kecha |
| R-03 | Ro'za hayiti | Fitr sadaqasi ogohlantirishi, namoz vaqti oynasi |
| R-04 | Qurbon hayiti | Takbir tashriq, qurbonlik vaqti |

---

## 4. TEXNIK STACK

| Qatlam | Texnologiya | Sabab |
|---|---|---|
| Bot | Python 3.12 + aiogram 3.x | Mavjud tajriba |
| Backend | FastAPI | Mini App uchun API |
| Baza | PostgreSQL + asyncpg | Railway'da tayyor |
| Rejalashtiruvchi | APScheduler | Bildirishnoma |
| Frontend | React + Vite | Prototip tayyor |
| Deploy | Railway | Mavjud infratuzilma |
| Scraper | httpx + BeautifulSoup | Yengil |

---

## 5. BOSQICHLI REJA — 4 HAFTA

### 0-BOSQICH · Tayyorgarlik (1–2 kun, parallel)

| Ish | Natija |
|---|---|
| namozvaqti.uz ga ruxsat xati yuborish | Javob kutiladi (bloklovchi emas) |
| Railway loyihasi + PostgreSQL | DATABASE_URL tayyor |
| GitHub repo | `namoz-bot` |
| BotFather'dan token | BOT_TOKEN |

**Muhim:** ruxsat javobini kutmasdan davom eting. Agar rad javob kelsa, Aladhan API ga o'tasiz — arxitektura buni ko'zda tutgan.

---

### 1-BOSQICH · Ma'lumot poydevori (3–4 kun)

**Natija:** bazada Xorazm 6 shahri uchun yillik jadval bor.

- [ ] Baza sxemasi (`shaharlar`, `namoz_vaqtlari`, `suralar`)
- [ ] Scraper ishga tushirish (`--toplam xorazm`)
- [ ] Ma'lumot to'g'riligini qo'lda tekshirish (3 kun tanlab, sayt bilan solishtirish)
- [ ] Suralar yuklash + mushaf bilan solishtirish
- [ ] Yirik shaharlarni qo'shish

**Tekshirish mezoni:** `SELECT * FROM namoz_vaqtlari WHERE shahar_id=1` → 365 qator.

---

### 2-BOSQICH · Bot yadrosi (4–5 kun)

**Natija:** bot javob beradi, vaqt ko'rsatadi.

- [ ] `/start` → maqsad so'rovi → shahar tanlash (inline tugmalar)
- [ ] Foydalanuvchi jadvali (`telegram_id`, `shahar_id`, `pozitsiya`, `daraja`)
- [ ] `/vaqt` — bugungi jadval + keyingi namozgacha
- [ ] `/sozlama`
- [ ] Railway'ga deploy

**Tekshirish mezoni:** o'zingiz botdan foydalanib bir kun o'tkazing.

---

### 3-BOSQICH · Bildirishnoma (4–5 kun) ⚠️ ENG MUHIM

**Natija:** bot o'z vaqtida eslatadi.

- [ ] APScheduler — har kuni 00:05 da kunlik vazifalarni rejalashtiradi
- [ ] Foydalanuvchi sozlamasi: qaysi namozlar + necha daqiqa oldin
- [ ] **Standart holat: kuniga 1 ta eslatma.** Foydalanuvchi o'zi ko'paytiradi
- [ ] Blok qilgan foydalanuvchini avtomatik o'chirish
- [ ] Xato bo'lsa qayta urinish

**Dizayn qoidasi:** kuniga 5 ta push yubormang. Foydalanuvchi charchaydi va botni o'chiradi. Ramazonda saharlik/iftor eslatmasi avtomatik yoqiladi — u yerda push haqiqatan zarur.

**Tekshirish mezoni:** 3 kun davomida eslatmalar to'g'ri vaqtda kelsin.

---

### 4-BOSQICH · Mini App (5–6 kun)

**Natija:** «Ilovani ochish» tugmasi ishlaydi.

- [ ] FastAPI endpointlari: `/api/vaqtlar`, `/api/foydalanuvchi`, `/api/suralar`
- [ ] Telegram initData tekshiruvi (xavfsizlik)
- [ ] Prototip UI ni real ma'lumotga ulash
- [ ] Bosh ekran + svetofor + halqa
- [ ] Suralar o'quvchi + qoida oynasi
- [ ] Manba yozuvi (huquqiy shart)

**Tekshirish mezoni:** telefonda ochib, bir kun ishlatib ko'ring.

---

### 5-BOSQICH · Rejimlar va qo'shimchalar (4–5 kun)

- [ ] Juma rejimi (masjid tanlash bilan)
- [ ] Ramazon rejimi (zanjir, taroveh, oxirgi o'n kecha)
- [ ] Hayit rejimlari
- [ ] Qasr logikasi (70 km + 7 kun)
- [ ] Qazo hisoblagichi

---

### 6-BOSQICH · Test va chiqarish (3–4 kun)

- [ ] 10–15 yaqin kishiga berib sinash
- [ ] Xatolarni tuzatish
- [ ] @Drfarrukhmission da e'lon

---

## 6. TOKEN TEJASH QOIDALARI

Bu loyiha uzoq davom etadi — kontekst boshqaruvi pul va vaqt tejaydi.

### 6.1 Har bosqich — alohida suhbat

Yangi bosqichga o'tganda **yangi chat oching.** Eski kontekstni sudrab yurmang. Boshida qisqa xulosa bering: «2-bosqich tugadi, bot ishlayapti. Endi bildirishnoma qilamiz.»

### 6.2 Fayllarni kichik tuting

Har fayl **200–300 qatordan oshmasin.** Siz to'liq fayl almashtirishni afzal ko'rasiz — bu to'g'ri yondashuv, lekin faqat fayl kichik bo'lsa arzon bo'ladi.

Modullarga bo'ling:
```
bot/
  handlers/start.py       ~150 qator
  handlers/vaqt.py        ~120 qator
  handlers/sozlama.py     ~150 qator
  services/vaqt_xizmat.py ~200 qator
  services/eslatma.py     ~250 qator
  db/models.py            ~180 qator
```

### 6.3 Xatolarni to'g'ri yuboring

Butun logni emas, **faqat traceback'ning oxirgi 15 qatorini** yuboring. Kerak bo'lsa qaysi fayl ekanini ayting, men o'sha faylni so'rayman.

### 6.4 Claude Code ishlating

Terminal orqali ishlaganda Claude Code fayllarni **to'g'ridan-to'g'ri tahrirlaydi** — butun faylni chatga nusxalash shart emas. Bu eng katta tejash manbai.

### 6.5 Prompt caching

Agar API orqali ishlasangiz, o'zgarmaydigan kontekstni (baza sxemasi, TZ) cache qiling — kirish narxi 90% gacha kamayadi.

---

## 7. MODEL TANLASH

**Bugungi holat (28 iyul 2026):** Anthropic'da to'rtta ochiq model bor.

| Model | Narx ($/MTok kirish/chiqish) | Bu loyihada |
|---|---|---|
| **Haiku 4.5** | $1 / $5 | Oddiy vazifalar, klassifikatsiya |
| **Sonnet 5** | $3 / $15 (**intro $2/$10** — 31 avgustgacha) | **Asosiy ish** |
| **Opus 5** | $5 / $25 | Arxitektura, murakkab debug |
| **Fable 5** | $10 / $50 | Bu loyihaga kerak emas |

### 7.1 Tavsiyam

**Sonnet 5 — asosiy model.** Kod yozish, bot handlerlari, API endpointlari, UI komponentlari — hammasi shu bilan. Ishlab chiqarish uchun mo'ljallangan asosiy model, tezligi va sifati muvozanatlangan.

**Muhim moliyaviy nuqta:** Sonnet 5 hozir kirish narxi $2, chiqish $10 — bu **kirish narxi 31 avgustda $3/$15 ga ko'tariladi.** Ya'ni loyihaning eng ko'p kod yoziladigan qismini (1–4 bosqichlar) **avgust oxirigacha tugatsangiz**, sezilarli tejaysiz. Sizning 4 haftalik rejangiz aynan shunga to'g'ri keladi.

**Opus 5 — tanlab.** Faqat quyidagilarda:
- Baza sxemasini yakuniy loyihalash
- Bildirishnoma rejalashtiruvchisining vaqt mantiqini tekshirish (eng xatoga moyil qism)
- Uzoq debug qilingan, yechilmayotgan xato

**Haiku 4.5** — agar ilova ichida AI ishlatsangiz (masalan, foydalanuvchi savoliga javob), yoki ko'p sonli bir xil vazifalar uchun.

### 7.2 Amaliy sxema

```
Arxitektura qarori      → Opus 5     (~5% ish)
Kod yozish              → Sonnet 5   (~85% ish)
Oddiy tuzatish, matn    → Haiku 4.5  (~10% ish)
```

---

## 8. XAVFLAR VA CHORALAR

| Xavf | Ehtimol | Chora |
|---|---|---|
| namozvaqti.uz ruxsat bermaydi | O'rta | Aladhan API ga o'tish, arxitektura tayyor |
| Sayt tuzilishi o'zgaradi | Past | Yillik yig'ish + zaxira manba |
| Qur'on matnida xato | **Yuqori ta'sir** | Bosma mushaf bilan tekshirish, `tasdiqlangan` bayrog'i |
| Fiqhiy noaniqlik (qasr, vaqt) | O'rta | «Ustozdan so'rang» eslatmasi, hukm bermaslik |
| Push charchoq → o'chirish | Yuqori | Standart 1 ta eslatma |
| Loyihaga qiziqish yo'qolishi | **Yuqori** | Har bosqich mustaqil qiymat beradi |

Oxirgi xavf haqida ochiq gapiraman: siz o'zingiz noldan qurishni yoqtirasiz, lekin loyiha rutinaga aylanganda qiziqish so'nadi. Shuning uchun reja shunday tuzilganki, **har bosqich o'zicha ishlaydigan narsa beradi.** 2-bosqichdan keyin botni ishlatishingiz mumkin, 4-bosqichdan keyin odamlarga ko'rsatasiz. Agar 5-bosqichda to'xtasangiz ham, qo'lingizda ishlaydigan mahsulot qoladi.

---

## 9. MUVAFFAQIYAT MEZONLARI

**4 hafta oxirida:**

- [ ] Bot ishlaydi, kamida 6 shahar qo'llab-quvvatlanadi
- [ ] Bildirishnoma o'z vaqtida keladi (±1 daqiqa)
- [ ] Mini App telefonda muammosiz ochiladi
- [ ] 20 ta sura oflayn o'qiladi
- [ ] Manba yozuvi har ekranda bor
- [ ] 10+ kishi sinovdan o'tkazgan

---

## 10. KEYINGI QADAM

Hoziroq boshlanadigan ikkita ish:

1. namozvaqti.uz ga xat yuborish (`t.me/namozvaqtiuz_bot`)
2. Railway'da PostgreSQL yaratish

Shundan so'ng 1-bosqich — scraper ishga tushiriladi.
