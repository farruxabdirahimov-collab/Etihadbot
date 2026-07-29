/** Rakat tuzilishi — umumiy, manbaga bog'liq bo'lmagan fiqhiy ma'lumot.
 * Zam sura tavsiyasi — sura RAQAMI orqali (nomi emas), API'dan kelgan
 * suralar ro'yxati bilan moslashtiriladi. */
export const NAMOZLAR = [
  {
    nom: "Bomdod", arab: "الفجر",
    rakat: [{ turi: "sunnat", soni: 2 }, { turi: "farz", soni: 2 }],
    sura: { boshlangich: 112, orta: 108, murakkab: 97 },
  },
  {
    nom: "Peshin", arab: "الظهر",
    rakat: [{ turi: "sunnat", soni: 4 }, { turi: "farz", soni: 4 }, { turi: "sunnat", soni: 2 }],
    sura: { boshlangich: 113, orta: 110, murakkab: 105 },
  },
  {
    nom: "Asr", arab: "العصر",
    rakat: [{ turi: "sunnat", soni: 4 }, { turi: "farz", soni: 4 }],
    sura: { boshlangich: 114, orta: 107, murakkab: 106 },
  },
  {
    nom: "Shom", arab: "المغرب",
    rakat: [{ turi: "farz", soni: 3 }, { turi: "sunnat", soni: 2 }],
    sura: { boshlangich: 112, orta: 103, murakkab: 104 },
  },
  {
    nom: "Xufton", arab: "العشاء",
    rakat: [{ turi: "sunnat", soni: 4 }, { turi: "farz", soni: 4 }, { turi: "sunnat", soni: 2 }, { turi: "vitr", soni: 3 }],
    sura: { boshlangich: 108, orta: 102, murakkab: 101 },
  },
];

export const NAMOZ_TARTIBI = ["bomdod", "peshin", "asr", "shom", "xufton"];

export const DARAJA_NOM = { boshlangich: "Boshlang'ich", orta: "O'rta", murakkab: "Murakkab" };

export const QOIDA = [
  { n: 1, nom: "Niyat", izoh: "Qaysi namozni o'qiyotganingizni ko'ngildan o'tkazasiz." },
  { n: 2, nom: "Takbiratul ihrom", izoh: "Qo'lni quloq barobariga ko'tarib «Allohu akbar» deysiz. Shundan so'ng namoz boshlandi — gapirmaysiz, o'girilmaysiz." },
  { n: 3, nom: "Qiyom", izoh: "Tik turib Fotiha surasini, so'ng zam surani o'qiysiz." },
  { n: 4, nom: "Ruku'", izoh: "Belni egib «Subhana Robbiyal Aziym» — uch marta." },
  { n: 5, nom: "Qavma", izoh: "Tik turasiz: «Samiy'allohu liman hamidah — Robbana lakal hamd»." },
  { n: 6, nom: "Sajda", izoh: "Peshona yerga tegadi: «Subhana Robbiyal A'la» — uch marta." },
  { n: 7, nom: "Jalsa", izoh: "Bir lahza o'tirasiz, so'ng ikkinchi sajdani qilasiz." },
  { n: 8, nom: "Ikkinchi rakat", izoh: "Turib 3–7-qadamlarni takrorlaysiz." },
  { n: 9, nom: "Qa'da", izoh: "O'tirib Attahiyot, salovot va duoni o'qiysiz." },
  { n: 10, nom: "Salom", izoh: "O'ngga, so'ng chapga qarab «Assalomu alaykum va rohmatulloh»." },
];
