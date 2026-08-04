/** Qurilma kompasi bilan ishlash.
 *
 * GPS kerak emas — joylashuv tanlangan shahardan olinadi. Bu yerda faqat
 * telefonning qaysi tomonga qaralganini bilish uchun orientatsiya sensori
 * ishlatiladi. iOS 13+ da bu foydalanuvchi harakatidan keyin ruxsat so'raydi,
 * Telegram WebView'da esa umuman ishlamasligi mumkin — shuning uchun
 * chaqiruvchi tomon har doim kompassiz holatni ham qo'llab-quvvatlashi kerak.
 */

function iosRuxsatKerakmi() {
  return typeof DeviceOrientationEvent !== "undefined"
    && typeof DeviceOrientationEvent.requestPermission === "function";
}

/** Kompasni ishga tushiradi. Muvaffaqiyatli bo'lsa tozalash funksiyasini,
 * aks holda null qaytaradi. */
export async function kompasniYoq(ozgardi) {
  if (typeof window === "undefined" || !window.DeviceOrientationEvent) return null;

  if (iosRuxsatKerakmi()) {
    try {
      const javob = await DeviceOrientationEvent.requestPermission();
      if (javob !== "granted") return null;
    } catch {
      return null;
    }
  }

  function ishlov(hodisa) {
    // iOS to'g'ridan-to'g'ri haqiqiy shimolga nisbatan yo'nalish beradi.
    if (typeof hodisa.webkitCompassHeading === "number") {
      ozgardi(hodisa.webkitCompassHeading);
      return;
    }
    // Android: alpha soat strelkasiga teskari sanaladi.
    if (typeof hodisa.alpha === "number") {
      ozgardi((360 - hodisa.alpha) % 360);
    }
  }

  const hodisaNomi = "ondeviceorientationabsolute" in window
    ? "deviceorientationabsolute"
    : "deviceorientation";
  window.addEventListener(hodisaNomi, ishlov, true);
  return () => window.removeEventListener(hodisaNomi, ishlov, true);
}
