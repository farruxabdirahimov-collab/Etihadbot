/** Telegram WebApp SDK bilan ishlash uchun yengil qobiq. */

function webApp() {
  return window.Telegram?.WebApp ?? null;
}

export function telegramniTayyorla() {
  const wa = webApp();
  if (!wa) return;
  wa.ready();
  wa.expand();
}

export function initDataOl() {
  return webApp()?.initData ?? "";
}

/** Telegram ichida ochilganmi? initData imzolangan ma'lumot bo'lgani
 * uchun uning mavjudligi ishonchli belgi — oddiy brauzerda u bo'sh. */
export function telegramdami() {
  return Boolean(initDataOl());
}

export function foydalanuvchiIdOl() {
  return webApp()?.initDataUnsafe?.user?.id ?? null;
}

/** Telegram'ning ulashish oynasini ochadi. Telegram tashqarisida (oddiy
 * brauzerda) yangi oynada ochilishi bilan cheklanadi. */
export function ulashishniOch(havola, matn) {
  const url = `https://t.me/share/url?url=${encodeURIComponent(havola)}&text=${encodeURIComponent(matn)}`;
  const wa = webApp();
  if (wa?.openTelegramLink) {
    wa.openTelegramLink(url);
  } else {
    window.open(url, "_blank");
  }
}
