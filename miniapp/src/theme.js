export const DISPLAY =
  "'Iowan Old Style', 'Palatino Linotype', Palatino, 'Book Antiqua', Georgia, serif";
export const UTIL = "ui-sans-serif, system-ui, -apple-system, 'Segoe UI', sans-serif";
export const ARAB = "'SF Arabic', 'Geeza Pro', 'Traditional Arabic', 'Scheherazade New', serif";

export const PALETTE = {
  yashil: { yuqori: "#16311B", past: "#0A1A0D", matn: "#F2EDE0", xira: "#93A38C", urgu: "#C9A961", holat: "Vaqt yetarli" },
  sariq: { yuqori: "#3E2A0C", past: "#241704", matn: "#F7EEDC", xira: "#B69C72", urgu: "#C9A961", holat: "Tayyorlanish vaqti" },
  qizil: { yuqori: "#3B1216", past: "#220709", matn: "#F7E9E5", xira: "#B08D85", urgu: "#C9A961", holat: "Vaqt kam qoldi" },
  tugadi: { yuqori: "#1C2320", past: "#0D1210", matn: "#EAEDE9", xira: "#8CA097", urgu: "#93A38C", holat: "Bugungi namozlar tugadi" },
};

const R = 108;
export const HALQA_RADIUS = R;
export const HALQA_UZUNLIK = 2 * Math.PI * R;

export function ikki(n) {
  return String(n).padStart(2, "0");
}
