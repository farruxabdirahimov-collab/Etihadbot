from fastapi import FastAPI

app = FastAPI(title="Namoz Bot Mini App API")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
