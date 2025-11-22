"""Routers exposing CRUD + AI helpers for items."""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

import crud
from database import get_db
from schemas import ItemCreate, ItemResponse, ItemUpdate
from schemas.chatgpt_schemas import ItemAnalysisResponse
from services.chatgpt_service import chatgpt_service
from config import settings

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not Found"}},
)


@router.post(
    "/{item_id}/analyze",
    response_model=ItemAnalysisResponse,
    summary="Проанализировать товар с помощью AI",
)
async def analyze_item(item_id: int, db: Session = Depends(get_db)):
    if not settings.OPENAI_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="ChatGPT service is not configured",
        )

    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    if not db_item.description:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item has no description")

    analysis = await chatgpt_service.analyze_item_description(db_item.description)
    titles = await chatgpt_service.generate_item_titles(db_item.description)

    if analysis is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="AI analysis failed")

    return ItemAnalysisResponse(
        original_description=db_item.description,
        analysis=analysis,
        generated_titles=titles or "Не удалось сгенерировать заголовки",
    )


@router.post(
    "/{item_id}/suggest-improvements",
    summary="AI рекомендации для описания товара",
)
async def suggest_improvements(item_id: int, db: Session = Depends(get_db)):
    if not settings.OPENAI_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="ChatGPT service is not configured",
        )

    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    if not db_item.description:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item has no description")

    prompt = (
        "Проанализируй описание товара и предложи улучшения: 1) 3 новых описания,"
        " 2) ключевые слова для SEO, 3) структуру текста, 4) призывы к действию. "
        f"Описание: {db_item.description}"
    )

    messages = [
        {"role": "system", "content": "Ты эксперт по маркетингу."},
        {"role": "user", "content": prompt},
    ]

    suggestions = await chatgpt_service.get_chat_completion(messages)
    return {
        "item_id": item_id,
        "original_description": db_item.description,
        "suggestions": suggestions or "Не удалось сгенерировать рекомендации",
    }


@router.post(
    "/",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать предмет",
)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db=db, item=item)


@router.get(
    "/",
    response_model=List[ItemResponse],
    summary="Получить список предметов",
)
def read_items(
    skip: int = Query(0, ge=0, description="Сколько записей пропустить"),
    limit: int = Query(100, ge=1, le=1000, description="Лимит записей"),
    title: Optional[str] = Query(None, description="Фильтр по названию"),
    db: Session = Depends(get_db),
):
    return crud.get_items(db, skip=skip, limit=limit, title_filter=title)


@router.get(
    "/{item_id}",
    response_model=ItemResponse,
    summary="Получить предмет по ID",
)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return db_item


@router.put(
    "/{item_id}",
    response_model=ItemResponse,
    summary="Обновить предмет",
)
def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)):
    db_item = crud.update_item(db, item_id=item_id, item=item)
    if db_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return db_item


@router.delete(
    "/{item_id}",
    summary="Удалить предмет",
)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    success = crud.delete_item(db, item_id=item_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return {"message": "Item deleted successfully"}
