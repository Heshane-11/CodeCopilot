import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from coding_assistant.api.router import api_router
from coding_assistant.api.routes.metrics_route import router as metrics_router
from coding_assistant.config import get_settings
from coding_assistant.db.session import init_db
from coding_assistant.routing.credentials import configure_litellm_credentials
from coding_assistant.observability import setup_observability
from coding_assistant.observability.middleware import ObservabilityMiddleware

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    settings = get_settings()
    logging.basicConfig(level=settings.log_level)
    configure_litellm_credentials(settings)
    setup_observability()
    await init_db()
    logger.info("Database initialized")
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="Coding Assistant API",
        version="0.1.0",
        description="Phase 1 core runtime — LangGraph orchestration with structured tools",
        lifespan=lifespan,
    )
    app.add_middleware(ObservabilityMiddleware)
    app.include_router(metrics_router)
    app.include_router(api_router)
    return app
