<div align="center">

# 🤖 CodeCopilot

### AI-Powered Coding Assistant — Think, Plan, Execute

[![Live Demo](https://img.shields.io/badge/Live%20Demo-codecopilot.onrender.com-6366f1?style=for-the-badge&logo=render&logoColor=white)](https://codecopilot.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.136-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![LangGraph](https://img.shields.io/badge/LangGraph-Orchestrated-FF6B35?style=for-the-badge)](https://langchain-ai.github.io/langgraph/)

**CodeCopilot is an intelligent agentic coding assistant that understands your codebase, plans actions, runs tools safely, and helps you ship software faster — powered by the LLM of your choice.**

[🚀 Try Live Demo](https://codecopilot.onrender.com) · [📖 Docs](docs/) · [🐛 Report Bug](https://github.com/Heshane-11/CodeCopilot/issues)

</div>

---

## ✨ Features

| Feature | Description |
| :--- | :--- |
| 🧠 **Agentic Reasoning** | LangGraph-powered agent loop that thinks step-by-step before acting |
| 🔍 **Codebase Understanding** | Semantic code indexing and retrieval using pgvector embeddings |
| 🛠️ **Safe Tool Execution** | Sandboxed tool execution (filesystem, build, test, shell) inside an isolated Docker container |
| 🔄 **Multi-Model Support** | Works with OpenAI GPT-4, Anthropic Claude, and Google Gemini via LiteLLM |
| 🎯 **Smart Model Routing** | Capability-aware routing — assigns the right model for planning, coding, or summarization tasks |
| ✅ **Approval Workflows** | Critical write operations require human approval before execution |
| 📊 **Observability** | Built-in OpenTelemetry tracing, Prometheus metrics, and Langfuse integration |
| 🌐 **Web UI** | Clean browser-based chat interface served directly by the FastAPI backend |
| 🔐 **Auth & Rate Limiting** | Optional JWT authentication and per-minute rate limiting |

---

## 🌐 Live Demo

> **Try CodeCopilot instantly in your browser — no setup required!**

**[https://codecopilot.onrender.com](https://codecopilot.onrender.com)**

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                   User (Browser / CLI)              │
└────────────────────────┬────────────────────────────┘
                         │  HTTP / SSE
┌────────────────────────▼────────────────────────────┐
│              FastAPI Control Plane API               │
│         /v1/runs  /v1/tools  /health  /metrics      │
└──────────┬────────────────────────────┬─────────────┘
           │                            │
┌──────────▼──────────┐    ┌────────────▼────────────┐
│   LangGraph Agent   │    │    PostgreSQL + pgvector  │
│  (Plan → Act → Obs) │    │   (Run history + index)  │
└──────────┬──────────┘    └─────────────────────────┘
           │
┌──────────▼──────────┐    ┌─────────────────────────┐
│   LiteLLM Router    │    │         Redis            │
│  GPT / Claude /     │    │   (Session cache &       │
│      Gemini         │    │    job queue)            │
└──────────┬──────────┘    └─────────────────────────┘
           │
┌──────────▼──────────┐
│   Docker Sandbox    │
│  (Safe tool runner) │
└─────────────────────┘
```

---

## ⚡ Quick Start (Local)

**Prerequisites:** Python 3.12+, Docker, uv (recommended)

### 1. Clone & Setup

```bash
git clone https://github.com/Heshane-11/CodeCopilot.git
cd CodeCopilot
```

### 2. Start Infrastructure

```bash
docker compose up -d          # Starts PostgreSQL + Redis
docker compose build sandbox  # Builds the secure sandbox image
```

### 3. Configure

```bash
cp .env.example .env
# Edit .env and add at least ONE of:
# OPENAI_API_KEY=sk-...
# ANTHROPIC_API_KEY=sk-ant-...
# GEMINI_API_KEY=AIza...
```

### 4. Install & Run

```bash
pip install -e ".[dev]"
coding-assistant serve
# Open http://127.0.0.1:8000 in your browser
```

### 5. Chat (Terminal)

```bash
# In a second terminal:
coding-assistant chat --workspace /path/to/your/repo
```

---

## 🔑 API Keys Setup

Choose at least one LLM provider:

| Provider | Environment Variable | Get Key |
| :--- | :--- | :--- |
| Google Gemini | `GEMINI_API_KEY` | [Google AI Studio](https://aistudio.google.com/apikey) |
| OpenAI | `OPENAI_API_KEY` | [OpenAI Platform](https://platform.openai.com/api-keys) |
| Anthropic Claude | `ANTHROPIC_API_KEY` | [Anthropic Console](https://console.anthropic.com/) |

---

## 🧩 Usage

### Web UI
Open [http://localhost:8000](http://localhost:8000) in your browser after starting the server. No additional setup required.

### Terminal Chat

```bash
coding-assistant chat --workspace /path/to/my/project
# Available slash commands:
# /workspace <path>  — Switch project directory
# /status            — Show current configuration
# /help              — List all commands
# /exit              — Quit
```

### REST API

```bash
# Start a new run
curl -X POST http://localhost:8000/v1/runs \
  -H 'Content-Type: application/json' \
  -d '{"workspace_root": "/path/to/repo", "message": "Explain the main entry points"}'

# View interactive API docs
open http://localhost:8000/docs
```

---

## 🤖 Model Routing

CodeCopilot uses a capability-based routing system to assign the best model for each task type.

```bash
# Check which model will be used for a task
curl 'http://localhost:8000/v1/routing/resolve?capability=planning&complexity=high'
```

**Gemini-only setup:**
```bash
ROUTING_CONFIG_PATH=routing.config.gemini.json
ROUTING_DEFAULT_MODEL=gemini/gemini-2.5-flash
```

Supported models: `gemini/gemini-2.5-flash`, `gemini/gemini-2.0-flash`, `gpt-4o`, `claude-3-5-sonnet`, and many more via [LiteLLM](https://docs.litellm.ai/docs/providers).

---

## 📁 Project Structure

```
CodeCopilot/
├── src/coding_assistant/
│   ├── api/            # FastAPI route handlers
│   ├── intelligence/   # LangGraph agent & planning
│   ├── tools/          # Tool registry & handlers
│   ├── sandbox/        # Docker sandbox runner
│   ├── routing/        # LiteLLM model router
│   ├── db/             # SQLAlchemy models & migrations
│   ├── services/       # Redis client, embeddings
│   └── observability/  # OpenTelemetry, Prometheus
├── web/                # Frontend HTML/CSS/JS
├── docs/               # Architecture documentation
├── Dockerfile          # Production Docker image
├── render.yaml         # Render Blueprint spec
└── docker-compose.yml  # Local development stack
```

---

## 📖 Documentation

- [Getting Started Guide](GETTING_STARTED.md)
- [Core Runtime](docs/phase-1-core-runtime.md)
- [Model Routing](docs/phase-2-model-routing.md)
- [Tool System](docs/phase-3-tool-system.md)
- [Sandbox & Security](docs/phase-4-sandbox.md)

---

## 📄 License

This project is open source. See [LICENSE](LICENSE) for details.

---

<div align="center">

Built with ❤️ using FastAPI, LangGraph, and LiteLLM

**[🌐 Live Demo](https://codecopilot.onrender.com) · [⭐ Star on GitHub](https://github.com/Heshane-11/CodeCopilot)**

</div>
