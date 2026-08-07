/* Etihat — E'tiqod: xizmat ishchisi (service worker).
 *
 * Ehtiyotkor kesh strategiyasi — yaqinda index.html keshda qolib ketib,
 * yangilanish yetib bormagan muammo bo'lgan edi:
 *   · HTML va API  — faqat tarmoqdan, hech qachon keshdan berilmaydi
 *   · hash-li fayllar (/assets/…) — keshdan, chunki fayl o'zgarsa nomi
 *     ham o'zgaradi, ya'ni eski nusxa hech qachon noto'g'ri bo'lmaydi
 *   · ikonkalar     — keshdan, tarmoq bo'lmasa ham ko'rinsin
 */

const KESH = "etihat-v1";

self.addEventListener("install", () => self.skipWaiting());

self.addEventListener("activate", (hodisa) => {
  hodisa.waitUntil(
    (async () => {
      const nomlar = await caches.keys();
      await Promise.all(nomlar.filter((n) => n !== KESH).map((n) => caches.delete(n)));
      await self.clients.claim();
    })()
  );
});

function keshlanadimi(url) {
  return url.pathname.startsWith("/assets/") || url.pathname.startsWith("/ikonka-");
}

self.addEventListener("fetch", (hodisa) => {
  const so_rov = hodisa.request;
  if (so_rov.method !== "GET") return;

  const url = new URL(so_rov.url);
  if (url.origin !== self.location.origin) return;

  // Namoz vaqtlari va sozlamalar har doim yangi bo'lishi shart.
  if (url.pathname.startsWith("/api/")) return;

  if (keshlanadimi(url)) {
    hodisa.respondWith(
      caches.match(so_rov).then(
        (keshdan) =>
          keshdan ||
          fetch(so_rov).then((javob) => {
            if (javob.ok) {
              const nusxa = javob.clone();
              caches.open(KESH).then((kesh) => kesh.put(so_rov, nusxa));
            }
            return javob;
          })
      )
    );
    return;
  }

  // Qolgani (asosan index.html) — tarmoqdan. Tarmoq yo'q bo'lsagina
  // oxirgi saqlangan nusxa beriladi.
  hodisa.respondWith(
    fetch(so_rov)
      .then((javob) => {
        if (javob.ok && so_rov.mode === "navigate") {
          const nusxa = javob.clone();
          caches.open(KESH).then((kesh) => kesh.put(so_rov, nusxa));
        }
        return javob;
      })
      .catch(() => caches.match(so_rov))
  );
});
