import { initDataOl } from "./telegram.js";

const ASOS_URL = import.meta.env.VITE_API_URL ?? "";

async function sorov(yol, { kerakAuth = false, usul = "GET", tana } = {}) {
  const sarlavhalar = {};
  if (kerakAuth) {
    sarlavhalar["X-Telegram-Init-Data"] = initDataOl();
  }
  if (tana !== undefined) {
    sarlavhalar["Content-Type"] = "application/json";
  }
  const javob = await fetch(`${ASOS_URL}${yol}`, {
    method: usul,
    headers: sarlavhalar,
    body: tana !== undefined ? JSON.stringify(tana) : undefined,
  });
  if (!javob.ok) {
    // Backend `detail` maydonida tushunarli sabab yuboradi (masalan
    // «60 soniyadan keyin urinib ko'ring») — uni foydalanuvchiga
    // ko'rsatish uchun o'qib olamiz.
    let sabab = `So'rov xatosi: ${javob.status}`;
    try {
      const xato = await javob.json();
      if (typeof xato?.detail === "string") sabab = xato.detail;
    } catch {
      /* JSON emas — standart matn qoladi */
    }
    throw new Error(sabab);
  }
  return javob.json();
}

export const api = {
  foydalanuvchi: () => sorov("/api/foydalanuvchi", { kerakAuth: true }),
  vaqtlar: (shaharId) => sorov(`/api/vaqtlar?shahar_id=${shaharId}`),
  suralar: () => sorov("/api/suralar"),
  sura: (raqam) => sorov(`/api/suralar/${raqam}`),
  qibla: (shaharId) => sorov(`/api/qibla?shahar_id=${shaharId}`),
  ilova: () => sorov("/api/ilova"),
  viloyatlar: () => sorov("/api/viloyatlar"),
  sozlamalar: () => sorov("/api/sozlamalar", { kerakAuth: true }),
  sozlamalarniYangila: (patch) =>
    sorov("/api/sozlamalar", { kerakAuth: true, usul: "PATCH", tana: patch }),
  fikrYubor: (matn) => sorov("/api/fikr", { kerakAuth: true, usul: "POST", tana: { matn } }),
};
