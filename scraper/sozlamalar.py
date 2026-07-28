import re

ASOS = "https://namozvaqti.uz"
MANBA_NOMI = "namozvaqti.uz"
MANBA_IZOHI = "«Book Media Nashr» nashriyoti taqvim kitobi asosida"

# So'rovlar orasidagi pauza (soniya). Saytni ortiqcha yuklamaslik uchun.
PAUZA = 1.5

# Bosqichma-bosqich boshlash uchun: avval Xorazm, keyin qolgani.
XORAZM = ["urganch", "xiva", "xonqa", "hazorasp", "shovot", "yangibozor"]

YIRIK_SHAHARLAR = [
    "toshkent", "samarqand", "buxoro", "namangan", "andijon", "fargona",
    "qarshi", "nukus", "termiz", "jizzax", "navoiy", "guliston", "qoqon",
    "margilon", "angren", "chirchiq", "olmaliq", "shahrisabz", "zarafshon",
]

OYLAR = {
    1: "Yanvar", 2: "Fevral", 3: "Mart", 4: "Aprel", 5: "May", 6: "Iyun",
    7: "Iyul", 8: "Avgust", 9: "Sentyabr", 10: "Oktyabr",
    11: "Noyabr", 12: "Dekabr",
}

VAQT_RE = re.compile(r"^\d{1,2}:\d{2}$")
