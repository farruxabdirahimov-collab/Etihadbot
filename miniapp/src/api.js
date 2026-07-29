import { initDataOl } from "./telegram.js";

const ASOS_URL = import.meta.env.VITE_API_URL ?? "";

async function sorov(yol, kerakAuth = false) {
  const sarlavhalar = {};
  if (kerakAuth) {
    sarlavhalar["X-Telegram-Init-Data"] = initDataOl();
  }
  const javob = await fetch(`${ASOS_URL}${yol}`, { headers: sarlavhalar });
  if (!javob.ok) {
    throw new Error(`So'rov xatosi: ${javob.status}`);
  }
  return javob.json();
}

export const api = {
  foydalanuvchi: () => sorov("/api/foydalanuvchi", true),
  vaqtlar: (shaharId) => sorov(`/api/vaqtlar?shahar_id=${shaharId}`),
  suralar: () => sorov("/api/suralar"),
  sura: (raqam) => sorov(`/api/suralar/${raqam}`),
};
