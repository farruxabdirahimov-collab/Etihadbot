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
    throw new Error(`So'rov xatosi: ${javob.status}`);
  }
  return javob.json();
}

export const api = {
  foydalanuvchi: () => sorov("/api/foydalanuvchi", { kerakAuth: true }),
  vaqtlar: (shaharId) => sorov(`/api/vaqtlar?shahar_id=${shaharId}`),
  suralar: () => sorov("/api/suralar"),
  sura: (raqam) => sorov(`/api/suralar/${raqam}`),
  viloyatlar: () => sorov("/api/viloyatlar"),
  sozlamalar: () => sorov("/api/sozlamalar", { kerakAuth: true }),
  sozlamalarniYangila: (patch) =>
    sorov("/api/sozlamalar", { kerakAuth: true, usul: "PATCH", tana: patch }),
};
