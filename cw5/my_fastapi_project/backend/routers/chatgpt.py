"""Router exposing ChatGPT-powered utilities."""
from fastapi import APIRouter, HTTPException, status

from config import settings
from schemas.chatgpt_schemas import (
    ChatGPTPrompt,
    ChatGPTResponse,
    ItemAnalysisRequest,
    ItemAnalysisResponse,
    TitleGenerationRequest,
    TitleGenerationResponse,
)
from services.chatgpt_service import chatgpt_service

router = APIRouter(
    prefix="/chatgpt",
    tags=["chatgpt"],
    responses={404: {"description": "Not Found"}},
)


def _ensure_ai_configured():
    if not settings.OPENAI_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="ChatGPT service is not configured",
        )


@router.post("/chat", response_model=ChatGPTResponse)
async def chat_with_gpt(prompt: ChatGPTPrompt):
    _ensure_ai_configured()
    response = await chatgpt_service.get_chat_completion(
        messages=prompt.messages,
        temperature=prompt.temperature,
        max_tokens=prompt.max_tokens,
    )
    if response is None:
        return ChatGPTResponse(success=False, error="Failed to get response from ChatGPT")
    return ChatGPTResponse(success=True, response=response)


@router.post("/analyze-item", response_model=ItemAnalysisResponse)
async def analyze_item_description(request: ItemAnalysisRequest):
    _ensure_ai_configured()
    analysis = await chatgpt_service.analyze_item_description(request.description)
    titles = await chatgpt_service.generate_item_titles(request.description)
    if analysis is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to analyze item description",
        )
    return ItemAnalysisResponse(
        original_description=request.description,
        analysis=analysis,
        generated_titles=titles or "Не удалось сгенерировать заголовки",
    )


@router.post("/generate-titles", response_model=TitleGenerationResponse)
async def generate_item_titles(request: TitleGenerationRequest):
    _ensure_ai_configured()
    generated_titles = await chatgpt_service.generate_item_titles(request.description)
    if generated_titles is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate titles",
        )
    return TitleGenerationResponse(
        original_description=request.description,
        generated_titles=generated_titles,
    )


@router.get("/health")
async def chatgpt_health_check():
    return {
        "service": "chatgpt",
        "status": "available" if settings.OPENAI_API_KEY else "not_configured",
        "model": settings.OPENAI_MODEL,
    }
