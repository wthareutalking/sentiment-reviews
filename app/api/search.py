from fastapi import APIRouter
from app.elastic import search_reviews

router = APIRouter(prefix="/search", tags=["search"])

@router.get("/")
async def search(
    q: str = None,
    sentiment: float = None,
    rating_min: int = None,
    product_id: int = None,
):
    """Полнотекстовый поиск по отзывам."""
    results = search_reviews(
        q=q,
        sentiment=sentiment,
        rating_min=rating_min,
        product_id=product_id,
    )
    return {"total": len(results), "results": results}