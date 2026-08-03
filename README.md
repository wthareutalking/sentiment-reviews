# SentimentReviews – сервис анализа отзывов

[![CI](https://github.com/твой-username/sentiment-reviews/actions/workflows/ci.yml/badge.svg)](https://github.com/твой-username/sentiment-reviews/actions)
[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.141.1-009688.svg)](https://fastapi.tiangolo.com/)
[![Elasticsearch](https://img.shields.io/badge/Elasticsearch-8.17.0-005571.svg)](https://www.elastic.co/)

Полнофункциональный микросервис для сбора, анализа и поиска отзывов с маркетплейсов. Сочетает асинхронный веб-фреймворк, фоновую обработку, NLP и полнотекстовый поиск под одной крышкой Docker Compose.

---

## Быстрый старт

```bash
git clone https://github.com/твой-username/sentiment-reviews.git
cd sentiment-reviews
docker compose up --build -d
После запуска откройте в браузере:

API: http://localhost:8000

Swagger UI: http://localhost:8000/docs

Prometheus: http://localhost:9090

Grafana: http://localhost:3030 (admin / admin)

Архитектура и стек
Компонент	Технология
API	FastAPI (async) + Pydantic v2
База данных	PostgreSQL 16 + SQLAlchemy 2.0 (async) + Alembic
Фоновые задачи	Celery + Redis (брокер и backend)
NLP	Transformers (RuBERT-tiny2)
Поиск	Elasticsearch 8 (анализатор русского языка)
Мониторинг	Prometheus + Grafana
Контейнеризация	Docker, docker-compose
CI/CD	GitHub Actions (автотесты)

API – основные эндпоинты
Все примеры ниже можно выполнить прямо в терминале (PowerShell) или через Swagger UI.

1. Запуск парсинга товара
powershell
Invoke-RestMethod -Uri http://localhost:8000/parse/ -Method Post -ContentType "application/json" -Body '{"url":"https://example.com/product"}'
Ответ: {"message": "Задача принята", "task_id": "..."} – задача уходит в Celery.

2. Аналитика продукта
powershell
Invoke-RestMethod -Uri http://localhost:8000/analytics/product/1
Возвращает количество отзывов, средний рейтинг и распределение тональности.

3. Полнотекстовый поиск по отзывам
powershell
Invoke-RestMethod -Uri "http://localhost:8000/search/?q=отличный&sentiment=0.8&rating_min=4"
Поддерживает фильтры: q, sentiment, rating_min, product_id. В ответе подсвечиваются совпадения.

4. Health-check и метрики
/health – статус сервиса

/metrics – метрики для Prometheus

Конфигурация
Все настройки передаются через переменные окружения (см. docker-compose.yml). Основные параметры:

Переменная	Назначение	По умолчанию
DATABASE_URL	Подключение к PostgreSQL	postgresql+asyncpg://postgres:postgres@db:5432/sentiment
CELERY_BROKER_URL	Брокер Celery	redis://redis:6379/0
ELASTICSEARCH_URL	URL Elasticsearch	http://elasticsearch:9200
При локальном запуске (без Docker) можно создать файл .env – будет использован python-dotenv.

Структура проекта

sentiment-reviews/
├── app/
│   ├── api/               # Роутеры FastAPI
│   │   ├── parse.py
│   │   ├── analytics.py
│   │   └── search.py
│   ├── models.py          # Модели SQLAlchemy
│   ├── db.py              # Асинхронный движок и сессии
│   ├── tasks.py           # Задачи Celery
│   ├── parser.py          # Парсер (заглушка)
│   ├── sentiment.py       # NLP (тональность)
│   ├── elastic.py         # Клиент Elasticsearch
│   └── main.py            # Точка входа FastAPI
├── alembic/               # Миграции Alembic
├── tests/                 # Тесты (pytest)
├── docker-compose.yml
├── Dockerfile
├── prometheus.yml         # Конфигурация Prometheus
├── requirements.txt
└── .github/workflows/ci.yml

Разработка и тестирование
Установка зависимостей (опционально)

python -m venv .venv
source .venv/bin/activate  
pip install -r requirements.txt
Запуск тестов

pytest -v --cov=app
CI пайплайн автоматически запускает тесты при каждом пуше в main, поднимая PostgreSQL, Redis и Elasticsearch.

Мониторинг
Prometheus собирает метрики FastAPI (запросы, время ответа, ошибки).

Grafana на порту 3030 (логин/пароль admin/admin). После входа добавьте источник данных Prometheus с URL http://prometheus:9090 и создайте дашборд.

Особенности проекта
Полностью асинхронный стек (FastAPI + async SQLAlchemy + asyncpg)

Фоновые задачи с отслеживанием состояния через Celery

NLP‑анализ тональности на русском языке с помощью Hugging Face Transformers

Полнотекстовый поиск с морфологическим анализатором (Russian analyzer)

Production‑ready мониторинг и алертинг (Prometheus + Grafana)

CI/CD с автоматическим запуском тестов в окружении, идентичном продакшену

Полная документация API через Swagger UI

Масштабируемость: воркеры Celery могут быть размножены под нагрузкой

Сделано с ❤️ и вниманием к production‑деталям.