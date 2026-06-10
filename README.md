# Coding Assistant

Hybrid coding assistant with a LangGraph orchestration loop, structured tool execution, and FastAPI control-plane API.

## Prerequisites

- Python 3.12+
- Docker (for PostgreSQL and Redis)

## Quick start

```bash
docker compose up -d
docker compose build sandbox-image
cp .env.example .env
# Set OPENAI_API_KEY, ANTHROPIC_API_KEY, and/or GEMINI_API_KEY in .env

pip install -e ".[dev]"
coding-assistant serve
```

API: http://127.0.0.1:8000/docs

## Terminal chat

In one terminal, start the server. In another, run the interactive client:

```bash
coding-assistant chat
# optional: --workspace /path/to/repo --api-url http://127.0.0.1:8000
```

Slash commands: `/help`, `/workspace <path>`, `/status`, `/exit`. Each line you type starts an agent run on the server.

## Create a run (HTTP)

```bash
curl -s -X POST http://127.0.0.1:8000/v1/runs \
  -H 'Content-Type: application/json' \
  -d '{"workspace_root": "/path/to/repo", "message": "List Python files in src"}'
```

## Architecture

```text
LLM → StructuredAction → Host Validation → Tool Execution
```

See [docs/phase-1-core-runtime.md](docs/phase-1-core-runtime.md) through [docs/phase-10-mcp-ecosystem.md](docs/phase-10-mcp-ecosystem.md), and [procedure.md](procedure.md).

Metrics: `GET http://127.0.0.1:8000/metrics`

## Model routing

Planner calls use capability-based routing (`routing.config.json`). Preview:

### Gemini (Google)

1. Set `GEMINI_API_KEY` in `.env` (from [Google AI Studio](https://aistudio.google.com/apikey)).
2. Either use the Gemini-first routing file:

   ```bash
   ROUTING_CONFIG_PATH=routing.config.gemini.json coding-assistant serve
   ```

   or override every tier with one model:

   ```bash
   ROUTING_DEFAULT_MODEL=gemini/gemini-2.5-flash coding-assistant serve
   ```

   The default `routing.config.json` also lists `gemini/gemini-2.0-flash` in `fallback_chain` after OpenAI/Anthropic.

   For Gemini-only setups, use `routing.config.gemini.json` (Gemini-only fallback chain; no OpenAI attempts).

Supported LiteLLM ids include `gemini/gemini-2.5-flash`, `gemini/gemini-2.0-flash`, and `gemini/text-embedding-004` (for `EMBEDDING_MODEL`).

```bash
curl -s 'http://127.0.0.1:8000/v1/routing/resolve?capability=planning&complexity=high'
```
