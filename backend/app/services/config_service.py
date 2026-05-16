from app.api.schemas import ConfigStatusResponse
from app.core.config import settings


def get_config_status() -> ConfigStatusResponse:
    return ConfigStatusResponse(
        service="Aurelia Ledger",
        llm_provider_configured=bool(settings.llm_api_key and settings.llm_base_url and settings.llm_model),
        embedding_configured=bool((settings.embedding_api_key or settings.llm_api_key) and settings.embedding_model),
        database_configured=bool(settings.database_url),
        qdrant_configured=bool(settings.qdrant_url),
        redis_configured=bool(settings.redis_url),
        fred_configured=bool(settings.fred_api_key),
        sec_user_agent_configured=bool(settings.sec_user_agent),
    )
