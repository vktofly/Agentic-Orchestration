# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-08-20

### Added
- **Enterprise Deployment**: Full Docker support with Next.js standalone build and multi-stage `uv` backend image.
- **Docker Compose Orchestration**: Unified `docker-compose.yml` for zero-configuration local deployment.
- **Dependency Inversion Vector Store**: Abstract interface for vector stores with implementations for `DummyRetriever` and `ChromaRetriever`, controlled via `VECTOR_STORE_TYPE` env var.
- **React Streaming Hook**: Custom `useAgentStream` hook in Next.js to encapsulate SSE streaming logic.

### Changed
- **Deep Modular Backend Architecture**: Extracted DSPy/LangGraph state and iteration logic from routers into a deep `src/graph/agent.py` orchestrator module.
- **UI Componentization**: Refactored massive `page.tsx` into reusable components (`ChatBubble`, `MessageInput`, `DiffViewer`, `ProviderSelect`).
- **Concurrent Checkpointer**: Replaced synchronous SQLite LangGraph checkpointer with `AsyncSqliteSaver` via `aiosqlite` for robust concurrent threadpool execution.

### Fixed
- **Numpy Deadlock**: Resolved circular initialization deadlocks in async pipeline caused by lazy loaded `numpy` modules through `chromadb`.
