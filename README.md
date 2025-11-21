# CortexOps

**AI-driven system intelligence layer that auto-documents, debugs, and explains enterprise backend services using LLM orchestration.**

## Overview

As organizations integrate microservices and AI agents, system complexity outpaces developer cognition. CortexOps addresses this by enabling teams to query, explain, and debug their own distributed systems in natural language.

## Features

- **/ingest**: Upload or connect live telemetry (OpenTelemetry integration).
- **/query**: Natural language queries over system graph.
- **/docs**: Auto-generated architecture documentation.
- **/rootcause**: LLM-driven analysis of incident logs.

## Architecture

- **Backend**: FastAPI + PostgreSQL + Redis + Docker
- **LLM Layer**: OpenRouter (GPT-3.5/4, Llama 3) via LangChain
- **Embeddings**: FastEmbed (Local, BGE-small)
- **Vector DB**: Qdrant
- **Frontend**: Next.js + Tailwind CSS + Shadcn/UI

## Getting Started

### Prerequisites

- Docker & Docker Compose
- OpenRouter API Key

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/harshit-singhania/cortexops-mvp.git
    cd cortexops-mvp
    ```

2.  Set up environment variables:
    Create `backend/.env` with:
    ```
    POSTGRES_SERVER=postgres
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    POSTGRES_DB=cortexops
    QDRANT_HOST=qdrant
    REDIS_HOST=redis
    OPENROUTER_API_KEY=your_openrouter_key_here
    ```

3.  Run with Docker Compose:
    ```bash
    docker compose up -d --build
    ```

4.  Start the Frontend:
    ```bash
    cd frontend
    npm install
    npm run build
    npm start
    ```

5.  Access the Application:
    - **Dashboard**: http://localhost:3000
    - API Docs: http://localhost:8000/docs
    - Qdrant Dashboard: http://localhost:6333/dashboard

## License

MIT
