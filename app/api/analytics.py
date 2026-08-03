from fastapi import APIRouter
from sqlalchemy import select, func, case  # ← добавлен case
from app.db import async_session
from app.models import Product, Review

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/product/{product_id}")
async def product_analytics(product_id: int):
    async with async_session() as session:
        product = await session.get(Product, product_id)
        if not product:
            return {"error": "Продукт не найден"}

        stmt = select(
            func.count(Review.id).label("total"),
            func.avg(Review.rating).label("avg_rating"),
            func.sum(case((Review.sentiment > 0.1, 1), else_=0)).label("positive"),
            func.sum(case((Review.sentiment < -0.1, 1), else_=0)).label("negative"),
            func.sum(case((Review.sentiment.between(-0.1, 0.1), 1), else_=0)).label("neutral"),
        ).where(Review.product_id == product_id)

        result = await session.execute(stmt)
        row = result.one()
        total = row.total
        avg_rating = round(row.avg_rating, 2) if row.avg_rating else None

        return {
            "product_id": product.id,
            "title": product.title,
            "total_reviews": total,
            "average_rating": avg_rating,
            "sentiment_distribution": {
                "positive": row.positive or 0,
                "negative": row.negative or 0,
                "neutral": row.neutral or 0
            }
        }