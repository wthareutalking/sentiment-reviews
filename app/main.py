import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import text
from app.db import engine
from app.api.parse import router as parse_router
from app.api.analytics import router as analytics_router
from app.api.search import router as search_router
from app.elastic import init_es
from prometheus_fastapi_instrumentator import Instrumentator

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Код при запуске
    try:
        init_es()
        logger.info("Elasticsearch инициализирован")
    except Exception as e:
        logger.error(f"Не удалось инициализировать Elasticsearch: {e}")
    yield
    # Код при завершении (если нужно)

app = FastAPI(title="SentimentReviews", version="0.1.0", lifespan=lifespan)

Instrumentator().instrument(app).expose(app)

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