from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.routes import router as api_router
from backend.routes_fikr import router as fikr_router
from backend.routes_sozlama import router as sozlama_router

app = FastAPI(title="Etihat — E'tiqod Mini App API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(api_router)
app.include_router(sozlama_router)
app.include_router(fikr_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


class KeshsizStatik(StaticFiles):
    """index.html hech qachon keshlanmasin.

    Vite build'i JS fayl nomiga hash qo'shadi (index-XXXX.js), shuning
    uchun ularni uzoq keshlash xavfsiz. Lekin index.html o'sha hash'ga
    ishora qiladi — u keshda qolsa, yangi deploy'dan keyin ham Telegram
    WebView eski JS'ni yuklashda davom etadi."""

    async def get_response(self, path, scope):
        javob = await super().get_response(path, scope)
        if path in ("index.html", ".", "") or path.endswith(".html"):
            javob.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            javob.headers["Pragma"] = "no-cache"
            javob.headers["Expires"] = "0"
        return javob


# Mini App frontend'ining tayyor build'i (miniapp/dist) shu yerdan
# statik fayl sifatida xizmat qilinadi — alohida hosting kerak emas.
# /api va /health yo'llari yuqorida ro'yxatga olingani uchun ular
# ustuvor bo'ladi, qolgan hammasi statik fayllarga tushadi.
_dist_yoli = Path(__file__).resolve().parent.parent / "miniapp" / "dist"
if _dist_yoli.exists():
    app.mount("/", KeshsizStatik(directory=_dist_yoli, html=True), name="miniapp")
