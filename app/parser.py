from typing import Dict, Any, List

async def fetch_product_data(url: str) -> Dict[str, Any]:
    """Заглушка парсера. Возвращает название товара и список отзывов."""
    return {
        "title": f"Тестовый товар {url[-10:]}",
        "reviews": [
            {"text": "Отличный товар, очень доволен!", "rating": 5, "published_at": None},
            {"text": "Ужасное качество, не советую.", "rating": 1, "published_at": None}
        ]
    }