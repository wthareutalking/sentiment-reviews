import asyncio
from celery import Celery
from app.db import async_session
from app.models import Product, Review
from app.parser import fetch_product_data
from app.sentiment import analyze_sentiment
from app.elastic import index_review
from sqlalchemy import select

celery_app = Celery(
    "sentiment_reviews",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
)

@celery_app.task(name="parse_product", bind=True)
def parse_product(self, url: str):
    async def _run():
        data = await fetch_product_data(url)
        async with async_session() as session:
            result = await session.execute(select(Product).where(Product.url == url))
            product = result.scalar_one_or_none()

            if not product:
                product = Product(url=url, title=data["title"])
                session.add(product)
                await session.flush()
            else:
                product.title = data["title"]

            new_reviews = 0
            for rev_data in data["reviews"]:
                existing = await session.execute(
                    select(Review).where(
                        Review.product_id == product.id,
                        Review.text == rev_data["text"],
                    )
                )
                if not existing.scalar_one_or_none():
                    sentiment = analyze_sentiment(rev_data["text"])
                    review = Review(
                        product_id=product.id,
                        text=rev_data["text"],
                        rating=rev_data["rating"],
                        published_at=rev_data["published_at"],
                        sentiment=sentiment
                    )
                    session.add(review)
                    await session.flush()  # получаем review.id

                    # Индексация в Elasticsearch
                    published_at_str = rev_data["published_at"].isoformat() if rev_data.get("published_at") else None
                    index_review(
                        review_id=review.id,
                        product_id=product.id,
                        text=rev_data["text"],
                        rating=rev_data["rating"],
                        sentiment=sentiment,
                        published_at=published_at_str,
                    )

                    new_reviews += 1

            await session.commit()
            return {
                "status": "success",
                "product_id": product.id,
                "new_reviews": new_reviews
            }

    loop = asyncio.get_event_loop()
    return loop.run_until_complete(_run())