import logging

from agents.extensions.models.litellm_model import LitellmModel

from app.core.settings import settings

logging.getLogger("LiteLLM").setLevel(logging.WARNING)


llm_model = LitellmModel(
    base_url=settings.OPENROUTER_BASE_URL,
    api_key=settings.OPENROUTER_API_KEY,
    model="openrouter/z-ai/glm-4.7-flash",
)
