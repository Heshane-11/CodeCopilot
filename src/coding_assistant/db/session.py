import asyncio
from collections.abc import AsyncGenerator
import logging
import ssl
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from coding_assistant.config import get_settings
from coding_assistant.db.base import Base

logger = logging.getLogger(__name__)

_engine = None
_session_factory: async_sessionmaker[AsyncSession] | None = None


def normalize_database_url(raw_url: str) -> tuple[str, dict]:
    """
    Ensure the URL uses the asyncpg driver and prepare appropriate connect_args (e.g. SSL).
    """
    url = raw_url
    if url.startswith("postgres://"):
        url = "postgresql+asyncpg://" + url[len("postgres://"):]
    elif url.startswith("postgresql://") and not url.startswith("postgresql+asyncpg://"):
        url = "postgresql+asyncpg://" + url[len("postgresql://"):]

    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)
    connect_args: dict = {}

    ssl_mode = query_params.pop("sslmode", [None])[0]
    ssl_param = query_params.pop("ssl", [None])[0]

    needs_ssl = (
        ssl_mode in ("require", "verify-ca", "verify-full")
        or ssl_param in ("require", "true", "1")
        or (
            parsed.hostname
            and (
                "render.com" in parsed.hostname
                or "supabase" in parsed.hostname
                or "neon.tech" in parsed.hostname
            )
        )
    )

    if needs_ssl:
        ssl_ctx = ssl.create_default_context()
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE
        connect_args["ssl"] = ssl_ctx
    elif ssl_mode == "disable" or ssl_param in ("false", "0", "disable"):
        connect_args["ssl"] = False

    new_query = urlencode(query_params, doseq=True)
    clean_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        new_query,
        parsed.fragment,
    ))
    return clean_url, connect_args


def _get_engine():
    global _engine, _session_factory
    if _engine is None:
        settings = get_settings()
        clean_url, connect_args = normalize_database_url(settings.database_url)
        _engine = create_async_engine(
            clean_url,
            connect_args=connect_args,
            pool_pre_ping=True,
            pool_recycle=300,
            echo=False,
        )
        _session_factory = async_sessionmaker(_engine, expire_on_commit=False)
    return _engine, _session_factory


async def init_db(max_retries: int = 6, retry_delay: float = 3.0) -> None:
    engine, _ = _get_engine()
    for attempt in range(1, max_retries + 1):
        try:
            async with engine.begin() as conn:
                await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
                await conn.run_sync(Base.metadata.create_all)
            logger.info("Database initialized successfully.")
            return
        except Exception as e:
            if attempt == max_retries:
                logger.error(
                    f"Failed to initialize database after {max_retries} attempts: {e}"
                )
                raise
            logger.warning(
                f"Database initialization attempt {attempt}/{max_retries} failed: {e}. "
                f"Retrying in {retry_delay}s (waiting for DB to be ready)..."
            )
            await asyncio.sleep(retry_delay)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    _, factory = _get_engine()
    assert factory is not None
    async with factory() as session:
        yield session

