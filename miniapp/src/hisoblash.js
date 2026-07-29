import { PALETTE } from "./theme.js";

// Fiqh: har bir namoz o'z vaqti kirgandan keyingi chegara kirguncha
// amal qiladi. Quyosh bilan Peshin orasida hech qaysi farz namozning
// vaqti faol emas — bu holat joriyNom=null bilan ifodalanadi.
const OYNALAR = [
  [null, "bomdod"],
  ["bomdod", "quyosh"],
  [null, "peshin"],
  ["peshin", "asr"],
  ["asr", "shom"],
  ["shom", "xufton"],
  ["xufton", null],
];

function vaqtQur(hozir, hhmm, ertagami = false) {
  const [soat, daqiqa] = hhmm.split(":").map(Number);
  const kun = new Date(hozir);
  if (ertagami) kun.setDate(kun.getDate() + 1);
  return new Date(kun.getFullYear(), kun.getMonth(), kun.getDate(), soat, daqiqa, 0);
}

/** Hozir qaysi namozning vaqti ichidamiz (yoki keyingisi kutilmoqda)
 * va shu oynaning tugash chegarasiga qancha qolganini hisoblaydi.
 * `boshlanishi` — halqa progressini hisoblash uchun oyna boshlanish vaqti
 * (agar ma'lum bo'lsa). */
export function joriyHolatniHisobla(vaqtlar, hozir) {
  if (!vaqtlar) return null;

  for (const [joriyNom, chegaraNom] of OYNALAR) {
    if (chegaraNom === null) {
      const chegaraVaqt = vaqtlar.ertangi_bomdod ? vaqtQur(hozir, vaqtlar.ertangi_bomdod, true) : null;
      return { joriyNom, chegaraNom: "bomdod", chegaraVaqt, boshlanishi: vaqtQur(hozir, vaqtlar.xufton) };
    }
    const chegaraVaqt = vaqtQur(hozir, vaqtlar[chegaraNom]);
    if (chegaraVaqt > hozir) {
      const boshlanishi = joriyNom ? vaqtQur(hozir, vaqtlar[joriyNom]) : null;
      return { joriyNom, chegaraNom, chegaraVaqt, boshlanishi };
    }
  }
  return null;
}

export function rangniAniqla(qolganSoniya) {
  if (qolganSoniya === null) return PALETTE.tugadi;
  const daqiqa = qolganSoniya / 60;
  if (daqiqa > 20) return PALETTE.yashil;
  if (daqiqa > 10) return PALETTE.sariq;
  return PALETTE.qizil;
}
