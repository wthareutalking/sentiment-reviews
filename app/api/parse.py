from fastapi import APIRouter
from pydantic import BaseModel
from app.tasks import parse_product

router = APIRouter(prefix="/parse", tags=["parsing"])

class ParseRequest(BaseModel):
    url: str

@router.post("/")
async def start_parse(request: ParseRequest):
    """Запускает парсинг товара в фоновом режиме."""
    task = parse_product.delay(request.url)
    return {"message": "Задача принята", "task_id": task.id}