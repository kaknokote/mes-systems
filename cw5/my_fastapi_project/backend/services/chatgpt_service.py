"""Wrapper around OpenAI client to keep FastAPI endpoints lean."""
from typing import Dict, List, Optional

import logging
from openai import OpenAI

from config import settings

logger = logging.getLogger(__name__)


class ChatGPTService:
    def __init__(self) -> None:
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None
        self.model = settings.OPENAI_MODEL

    async def get_chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 512,
    ) -> Optional[str]:
        if not self.client:
            logger.warning("ChatGPT client not configured")
            return None

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content
        except Exception as exc:  # pragma: no cover - network errors
            logger.error("ChatGPT API call failed: %s", exc)
            return None

    async def analyze_item_description(self, description: str) -> Optional[str]:
        prompt = (
            "Проанализируй описание товара и предоставь краткий отчет по пунктам: "
            "1) ключевые характеристики, 2) целевая аудитория, 3) рекомендации, 4) оценка (1-10). "
            f"Описание: {description}"
        )
        messages = [
            {"role": "system", "content": "Ты помощник по анализу товаров."},
            {"role": "user", "content": prompt},
        ]
        return await self.get_chat_completion(messages)

    async def generate_item_titles(self, description: str) -> Optional[str]:
        prompt = (
            "Создай 3 коротких привлекательных заголовка (до 60 символов) для следующего товара. "
            "Разные стили и без повторов. "
            f"Описание: {description}"
        )
        messages = [
            {"role": "system", "content": "Ты специалист по маркетингу."},
            {"role": "user", "content": prompt},
        ]
        return await self.get_chat_completion(messages)


chatgpt_service = ChatGPTService()
