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

export function foydalanuvchiIdOl() {
  return webApp()?.initDataUnsafe?.user?.id ?? null;
}
