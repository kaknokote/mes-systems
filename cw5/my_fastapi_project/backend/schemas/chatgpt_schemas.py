"""Pydantic schemas dedicated to ChatGPT-related endpoints."""
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class ChatGPTPrompt(BaseModel):
    messages: List[Dict[str, str]] = Field(...)
    temperature: float = Field(0.7, ge=0.0, le=1.0)
    max_tokens: int = Field(512, ge=1, le=4096)


class ChatGPTResponse(BaseModel):
    success: bool
    response: Optional[str] = None
    error: Optional[str] = None


class ItemAnalysisRequest(BaseModel):
    description: str = Field(..., min_length=10)


class ItemAnalysisResponse(BaseModel):
    original_description: str
    analysis: str
    generated_titles: str


class TitleGenerationRequest(BaseModel):
    description: str = Field(..., min_length=10)
    style: Optional[str] = Field(None, description="Optional hint for tone")


class TitleGenerationResponse(BaseModel):
    original_description: str
    generated_titles: str
