"""Pydantic schemas for CRUD operations."""
from typing import Optional

from pydantic import BaseModel, Field


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
