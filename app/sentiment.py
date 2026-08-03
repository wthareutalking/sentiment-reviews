from transformers import pipeline
import logging

logger = logging.getLogger(__name__)
_sentiment_pipeline = None

def get_sentiment_pipeline():
    global _sentiment_pipeline
    if _sentiment_pipeline is None:
        logger.info("Загружаю модель sentiment-analysis...")
        _sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model="seara/rubert-tiny2-russian-sentiment",
            tokenizer="seara/rubert-tiny2-russian-sentiment"
        )
    return _sentiment_pipeline

def analyze_sentiment(text: str) -> float:
    if not text.strip():
        return 0.0
    pipe = get_sentiment_pipeline()
    result = pipe(text[:512])[0]
    label = result["label"]
    score = result["score"]
    if label == "negative":
        return -score
    elif label == "positive":
        return score
    else:
        return 0.0