"""Schemas package for FastAPI application."""
from typing import Optional

from pydantic import BaseModel, Field

from schemas.chatgpt_schemas import (
    ChatGPTPrompt,
    ChatGPTResponse,
    ItemAnalysisRequest,
    ItemAnalysisResponse,
    TitleGenerationRequest,
    TitleGenerationResponse,
)


class ItemBase(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[int] = Field(None, ge=0)


class ItemCreate(ItemBase):
    title: str = Field(..., min_length=1, max_length=100)


class ItemUpdate(ItemBase):
    pass


class ItemResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    price: Optional[int]

    class Config:
        from_attributes = True


__all__ = [
    "ItemBase",
    "ItemCreate",
    "ItemUpdate",
    "ItemResponse",
    "ChatGPTPrompt",
    "ChatGPTResponse",
    "ItemAnalysisRequest",
    "ItemAnalysisResponse",
    "TitleGenerationRequest",
    "TitleGenerationResponse",
]
