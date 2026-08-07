/** Mehmon rejimidagi sozlamalar — qurilma xotirasida (localStorage).
 *
 * Telegram ichida ochilganda sozlamalar serverda saqlanadi, chunki
 * bildirishnomani bot yuboradi. Telegram tashqarisida (sayt yoki bosh
 * ekranga qo'shilgan PWA) foydalanuvchini aniqlash imkoni yo'q, shuning
 * uchun tanlov shu qurilmaning o'zida qoladi.
 */

const KALIT = "etihat.sozlamalar";

const STANDART = {
  shahar_id: null,
  daraja: "boshlangich",
};

export function ol() {
  try {
    const xom = localStorage.getItem(KALIT);
    return xom ? { ...STANDART, ...JSON.parse(xom) } : { ...STANDART };
  } catch {
    // Shaxsiy rejim yoki xotira o'chirilgan — standart bilan davom etamiz.
    return { ...STANDART };
  }
}

export function yoz(patch) {
  const yangi = { ...ol(), ...patch };
  try {
    localStorage.setItem(KALIT, JSON.stringify(yangi));
  } catch {
    /* saqlab bo'lmadi — sessiya davomida baribir ishlaydi */
  }
  return yangi;
}
