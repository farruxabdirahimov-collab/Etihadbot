"""O'zbekistonning hududiy bo'linishi va har biriga tegishli shahar
slug'lari (scraper.sozlamalar dagi XORAZM va YIRIK_SHAHARLAR asosida).

Barcha viloyatlar foydalanuvchiga teng huquqli ko'rsatiladi — hech
biri boshqasidan "asosiy" yoki "mahalliy" deb ajratilmaydi."""

VILOYATLAR = {
    "Toshkent shahri": ["toshkent"],
    "Toshkent viloyati": ["angren", "chirchik", "olmaliq"],
    "Samarqand viloyati": ["samarqand"],
    "Buxoro viloyati": ["buxoro"],
    "Namangan viloyati": ["namangan"],
    "Andijon viloyati": ["andijon"],
    "Farg'ona viloyati": ["fargona", "qoqon", "margilon"],
    "Qashqadaryo viloyati": ["qarshi", "shahrisabz"],
    "Qoraqalpog'iston Respublikasi": ["nukus"],
    "Surxondaryo viloyati": ["termiz"],
    "Jizzax viloyati": ["jizzax"],
    "Navoiy viloyati": ["navoiy", "zarafshon"],
    "Sirdaryo viloyati": ["guliston"],
    "Xorazm viloyati": ["urganch", "xiva", "xonqa", "hazorasp", "shovot", "yangibozor"],
}

# Callback_data'da indeks sifatida ishlatish uchun barqaror tartib.
VILOYAT_TARTIBI = list(VILOYATLAR.keys())
