# Etihadbot — Namoz vaqtlari va o'rgatuvchi Telegram bot

Namoz vaqtlari + o'rgatuvchi Telegram bot va Mini App. Manba:
namozvaqti.uz — «Book Media Nashr» taqvim kitobi asosida.

## Texnik stack

- Python 3.12, aiogram 3.x — bot
- FastAPI — Mini App backend
- PostgreSQL + asyncpg (SQLAlchemy async) — baza
- APScheduler — bildirishnoma rejalashtiruvchisi
- React + Vite — Mini App frontend
- Deploy: Railway

## Loyiha tuzilishi

```
bot/            aiogram bot (handlerlar, config, baza ulanishi)
backend/        FastAPI Mini App backend
miniapp/        React + Vite frontend (reference/ — UI namunasi)
scraper/        namozvaqti.uz dan ma'lumot yig'uvchi skript
docs/           TZ.md va boshqa hujjatlar
```

## Ishga tushirish (lokal)

```bash
pip install -r requirements.txt
cp .env.example .env   # BOT_TOKEN va DATABASE_URL ni to'ldiring
python -m bot.main
```

## Bosqichlar

0. Tayyorgarlik — Railway, GitHub, bot token (**joriy bosqich**)
1. Ma'lumot poydevori — scraper, baza, Xorazm 6 shahri
2. Bot yadrosi — /start, /vaqt, shahar tanlash
3. Bildirishnoma — APScheduler, standart 1 ta eslatma/kun
4. Mini App — FastAPI + React ulash
5. Rejimlar — Juma, Ramazon, Hayit, qasr, qazo
6. Test va chiqarish
