"""Qo'llab-quvvatlanadigan shaharlarning taxminiy markaz koordinatalari.

Qibla yo'nalishini hisoblash uchun ishlatiladi — GPS ruxsati kerak emas,
chunki foydalanuvchi shahrini allaqachon tanlagan. Shahar ichidagi bir
necha kilometr farq qibla burchagiga sezilarli ta'sir qilmaydi (1 gradusdan
kam), lekin bu baribir taxminiy qiymat.
"""

# slug -> (kenglik, uzunlik)
SHAHAR_KOORDINATALARI: dict[str, tuple[float, float]] = {
    # Xorazm viloyati
    "urganch": (41.5500, 60.6333),
    "xiva": (41.3775, 60.3639),
    "xonqa": (41.4783, 60.7906),
    "hazorasp": (41.3200, 61.0739),
    "shovot": (41.6500, 60.4667),
    "yangibozor": (41.6167, 60.6167),
    # Yirik shaharlar
    "toshkent": (41.2995, 69.2401),
    "samarqand": (39.6270, 66.9750),
    "buxoro": (39.7681, 64.4556),
    "namangan": (40.9983, 71.6726),
    "andijon": (40.7821, 72.3442),
    "fargona": (40.3864, 71.7864),
    "qarshi": (38.8606, 65.7889),
    "nukus": (42.4531, 59.6103),
    "termiz": (37.2242, 67.2783),
    "jizzax": (40.1158, 67.8422),
    "navoiy": (40.0844, 65.3792),
    "guliston": (40.4897, 68.7842),
    "qoqon": (40.5286, 70.9425),
    "margilon": (40.4711, 71.7247),
    "angren": (41.0167, 70.1436),
    "chirchik": (41.4689, 69.5822),
    "olmaliq": (40.8447, 69.5983),
    "shahrisabz": (39.0575, 66.8300),
    "zarafshon": (41.5786, 64.2019),
}
