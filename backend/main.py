from fastapi import FastAPI

app = FastAPI(title="Etihat — E'tiqod Mini App API")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
