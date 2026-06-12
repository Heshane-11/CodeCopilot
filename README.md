# CodeCopilot: Intelligent Coding Assistant

An AI-powered coding assistant that understands your codebase and helps you build software faster. Built with LangGraph orchestration, structured tool execution, and a FastAPI control-plane API.

## What It Does

✨ **Code Understanding** - Analyzes and indexes your repository
🔧 **Tool Integration** - Runs safe tool commands (filesystem, build, test, etc.)
🎯 **Structured Reasoning** - Uses LLMs with approval workflows for critical operations
📊 **Observability** - Built-in tracing and metrics for debugging and monitoring

## Quick Start (5 minutes)

**Prerequisites:** Python 3.12+, Docker

1. **Setup Services**
   ```bash
   docker compose up -d
   docker compose build sandbox-image
   ```

2. **Configure Credentials**
   ```bash
   cp .env.example .env
   # Edit .env and add at least one API key:
   # OPENAI_API_KEY, ANTHROPIC_API_KEY, or GEMINI_API_KEY
   ```

3. **Install & Run**
   ```bash
   pip install -e ".[dev]"
   coding-assistant serve
   ```

4. **Chat (in another terminal)**
   ```bash
   coding-assistant chat --workspace /path/to/your/repo
   ```

## Usage Examples

### Interactive Terminal Chat

```bash
# Start server in terminal 1
coding-assistant serve

# Chat in terminal 2
coding-assistant chat --workspace /path/to/my/project
# Type: "List all Python files"
# Type: "/help" for available slash commands
```

### HTTP API

```bash
# Create a run
curl -s -X POST http://127.0.0.1:8000/v1/runs \
  -H 'Content-Type: application/json' \
  -d '{
    "workspace_root": "/path/to/repo",
    "message": "What are the main entry points in this project?"
  }'

# View API docs at: http://127.0.0.1:8000/docs
```

### Slash Commands

In terminal chat, use:
- `/workspace <path>` - Change project directory
- `/status` - Show current settings
- `/help` - List available commands
- `/exit` or `/quit` - Quit the client

## Architecture

```
User Input
    ↓
LLM (Claude, GPT, Gemini)
    ↓
Structured Action Generation
    ↓
Host Validation & Approval
    ↓
Tool Execution (safe sandbox)
    ↓
Response & Learning
```

## Cloud Deployment

CodeCopilot is designed to be fully cloud-ready and deployable on platforms like Render, Railway, or any VPS.

### Required Environment Variables

When deploying to the cloud, configure the following environment variables in your provider's dashboard:
- `DATABASE_URL`: Connection string to your cloud PostgreSQL database (pgvector must be enabled).
- `REDIS_URL`: Connection string to your cloud Redis instance.
- `GEMINI_API_KEY` (or `OPENAI_API_KEY` / `ANTHROPIC_API_KEY`): API key for the LLM.
- `ROUTING_CONFIG_PATH`: Set to `routing.config.gemini.json` for a Gemini-only setup.
- `ROUTING_DEFAULT_MODEL`: Set to `gemini/gemini-3.1-flash-lite` (or your preferred model).

---

### Option 1: Render (One-Click Blueprint)

You can deploy CodeCopilot with its database and cache automatically on Render using the provided `render.yaml` Blueprint:
1. Push this repository to your GitHub account.
2. In the Render Dashboard, click **New** -> **Blueprint**.
3. Select your repository.
4. Render will parse `render.yaml` and configure:
   - The FastAPI web service (running the `Dockerfile`).
   - A Redis cache instance.
   - A PostgreSQL database (Render supports `pgvector` out-of-the-box).
5. Enter your `GEMINI_API_KEY` when prompted and deploy.

---

### Option 2: Railway Deployment

Railway supports deploying directly via Dockerfile:
1. Link your GitHub repository to Railway.
2. Create a PostgreSQL service and a Redis service in your Railway project.
3. Add a new service from your CodeCopilot repository. Railway will automatically build the `Dockerfile`.
4. Bind variables in the app service:
   - Set `DATABASE_URL` to `${{Postgres.DATABASE_URL}}` (or corresponding Railway Postgres connection string)
   - Set `REDIS_URL` to `redis://default:${{Redis.REDISPASSWORD}}@${{Redis.REDISHOST}}:${{Redis.REDISPORT}}/0`
   - Add your API keys (`GEMINI_API_KEY`, etc.) and routing configs.
5. Deploy the application.

---

### Option 3: VPS Deployment (Docker Compose)

To deploy on a Virtual Private Server (VPS):
1. Clone this repository to your VPS.
2. Setup your `.env` file with your production API keys, production database URL, and Redis URL.
3. Start the services using Docker Compose:
   ```bash
   docker compose up -d --build
   ```

## For Developers

- **Core Runtime:** [docs/phase-1-core-runtime.md](docs/phase-1-core-runtime.md)
- **Model Routing:** [docs/phase-2-model-routing.md](docs/phase-2-model-routing.md)
- **Tool System:** [docs/phase-3-tool-system.md](docs/phase-3-tool-system.md)
- **Sandbox & Security:** [docs/phase-4-sandbox.md](docs/phase-4-sandbox.md)
- **Full Roadmap:** See [docs/](docs/) directory

See [GETTING_STARTED.md](GETTING_STARTED.md) for detailed setup guide.

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
