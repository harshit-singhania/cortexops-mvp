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
- **LLM Layer**: OpenAI GPT-4/5 via LangChain
- **Vector DB**: Qdrant
- **Frontend**: Next.js (Planned)

## Getting Started

### Prerequisites

- Docker & Docker Compose
- OpenAI API Key

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
    OPENAI_API_KEY=your_key_here
    ```

3.  Run with Docker Compose:
    ```bash
    docker compose up -d --build
    ```

4.  Access the API:
    - API Docs: http://localhost:8000/docs
    - Qdrant Dashboard: http://localhost:6333/dashboard

## License

MIT
