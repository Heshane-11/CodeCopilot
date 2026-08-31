import pytest
from coding_assistant.db.session import normalize_database_url


def test_normalize_postgres_scheme():
    url, connect_args = normalize_database_url("postgres://user:pass@localhost:5432/testdb")
    assert url == "postgresql+asyncpg://user:pass@localhost:5432/testdb"
    assert connect_args == {}


def test_normalize_postgresql_scheme():
    url, connect_args = normalize_database_url("postgresql://user:pass@localhost:5432/testdb")
    assert url == "postgresql+asyncpg://user:pass@localhost:5432/testdb"
    assert connect_args == {}


def test_normalize_render_external_url_with_ssl():
    raw = "postgres://user:pass@dpg-abc12345-a.oregon-postgres.render.com:5432/assistant?sslmode=require"
    url, connect_args = normalize_database_url(raw)
    assert url.startswith("postgresql+asyncpg://user:pass@dpg-abc12345-a.oregon-postgres.render.com:5432/assistant")
    assert "sslmode" not in url
    assert "ssl" in connect_args
    assert connect_args["ssl"] is not None


def test_normalize_ssl_disabled():
    raw = "postgresql+asyncpg://user:pass@localhost:5432/assistant?sslmode=disable"
    url, connect_args = normalize_database_url(raw)
    assert "sslmode" not in url
    assert connect_args.get("ssl") is False
