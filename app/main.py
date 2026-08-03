from fastapi import FastAPI
from app.db import engine
from sqlalchemy import text
from app.api.parse import router as parse_router
from app.api.analytics import router as analytics_router
from app.api.search import router as search_router
from app.elastic import init_es
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="SentimentReviews", version="0.1.0")

Instrumentator().instrument(app).expose(app)

@app.on_event("startup")
async def startup():
    init_es()

app.include_router(parse_router)
app.include_router(analytics_router)
app.include_router(search_router)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/db-check")
async def db_check():
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT 1"))
        return {"db_ok": result.scalar() == 1}