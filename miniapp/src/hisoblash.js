import { NAMOZ_TARTIBI } from "./data.js";
import { PALETTE } from "./theme.js";

function bugungiVaqt(hozir, hhmm) {
  const [soat, daqiqa] = hhmm.split(":").map(Number);
  return new Date(hozir.getFullYear(), hozir.getMonth(), hozir.getDate(), soat, daqiqa, 0);
}

/** Vaqtlar (bomdod..xufton) va hozirgi vaqt asosida keyingi namozni topadi. */
export function keyingiNamozniHisobla(vaqtlar, hozir) {
  if (!vaqtlar) return null;
  for (let i = 0; i < NAMOZ_TARTIBI.length; i++) {
    const nom = NAMOZ_TARTIBI[i];
    const toliqVaqt = bugungiVaqt(hozir, vaqtlar[nom]);
    if (toliqVaqt > hozir) {
      const oldingi = i > 0 ? bugungiVaqt(hozir, vaqtlar[NAMOZ_TARTIBI[i - 1]]) : null;
      return { indeks: i, nom, vaqt: toliqVaqt, oldingiVaqt: oldingi };
    }
  }
  return null; // bugungi barcha namozlar o'tgan
}

export function rangniAniqla(qolganSoniya) {
  if (qolganSoniya === null) return PALETTE.tugadi;
  const daqiqa = qolganSoniya / 60;
  if (daqiqa > 20) return PALETTE.yashil;
  if (daqiqa > 10) return PALETTE.sariq;
  return PALETTE.qizil;
}
