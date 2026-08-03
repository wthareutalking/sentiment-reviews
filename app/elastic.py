import os
import time
import logging
from elasticsearch import Elasticsearch, ConnectionError

logger = logging.getLogger(__name__)

ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
INDEX_NAME = "reviews"

es_client = None

def get_es_client():
    global es_client
    if es_client is None:
        # Ждём готовности Elasticsearch
        for attempt in range(30):
            try:
                es_client = Elasticsearch(ELASTICSEARCH_URL)
                if es_client.ping():
                    break
            except ConnectionError:
                logger.warning(f"Elasticsearch not ready, attempt {attempt+1}/30")
                time.sleep(2)
        else:
            raise Exception("Elasticsearch did not become ready")
    return es_client

def init_es():
    """Создаёт индекс с маппингом, если его нет."""
    es = get_es_client()
    if not es.indices.exists(index=INDEX_NAME):
        es.indices.create(
            index=INDEX_NAME,
            body={
                "mappings": {
                    "properties": {
                        "product_id": {"type": "integer"},
                        "text": {"type": "text", "analyzer": "russian"},
                        "rating": {"type": "integer"},
                        "sentiment": {"type": "float"},
                        "published_at": {"type": "date", "format": "yyyy-MM-dd"},
                    }
                }
            }
        )

def index_review(review_id: int, product_id: int, text: str, rating: int, sentiment: float, published_at: str):
    es = get_es_client()
    doc = {
        "product_id": product_id,
        "text": text,
        "rating": rating,
        "sentiment": sentiment,
        "published_at": published_at,
    }
    es.index(index=INDEX_NAME, id=str(review_id), body=doc)

def search_reviews(q: str = None, sentiment: float = None, rating_min: int = None, product_id: int = None):
    es = get_es_client()
    must = []
    filters = []

    if q:
        must.append({"match": {"text": q}})
    if sentiment is not None:
        filters.append({"term": {"sentiment": sentiment}})
    if rating_min is not None:
        filters.append({"range": {"rating": {"gte": rating_min}}})
    if product_id is not None:
        filters.append({"term": {"product_id": product_id}})

    body = {
        "query": {
            "bool": {
                "must": must,
                "filter": filters,
            }
        },
        "highlight": {
            "fields": {"text": {}}
        }
    }

    result = es.search(index=INDEX_NAME, body=body)
    hits = result["hits"]["hits"]
    return [
        {
            "review_id": hit["_id"],
            "score": hit["_score"],
            "source": hit["_source"],
            "highlight": hit.get("highlight", {}),
        }
        for hit in hits
    ]