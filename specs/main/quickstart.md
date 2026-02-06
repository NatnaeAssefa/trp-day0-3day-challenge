# Quickstart — Project Chimera Core

**Branch**: `main`  
**Phase**: 1 (Design)  
**Audience**: Developers implementing features 001–008.

This quickstart gets you from clone to running tests and understanding where specs and contracts live.

---

## 1. Prerequisites

- **Python**: 3.11+
- **Package manager**: [uv](https://docs.astral.sh/uv/) preferred, or `pip`
- **Docker**: Optional; used by `make test` to run tests in a container

---

## 2. Setup

From the repository root:

```bash
# Install dependencies (uv)
uv sync

# Or with pip
pip install -e .
```

Constitution and tooling: see [.specify/memory/constitution.md](../../.specify/memory/constitution.md) and [research/tooling_strategy.md](../../research/tooling_strategy.md).

---

## 3. Run tests

```bash
# Run tests (recommended: via Docker per Makefile)
make test
# Builds image and runs: docker run --rm chimera

# Or run pytest directly
pytest
```

Tests live under `tests/`. Contract tests should assert against [specs/technical.md](../technical.md) and the JSON contracts in [specs/main/contracts/](contracts/).

---

## 4. Spec and contract locations

| What | Where |
|------|--------|
| Vision and constraints | [specs/_meta.md](../_meta.md) |
| User stories and FRs | [specs/functional.md](../functional.md) |
| API contracts, ERD, MCP | [specs/technical.md](../technical.md) |
| This plan and design artifacts | **specs/main/** (plan.md, research.md, data-model.md, quickstart.md, contracts/) |
| Feature specs (001–008) | specs/001-trend-fetch-mcp/ … specs/008-openclaw-agent-status/ |
| Data model summary | [specs/main/data-model.md](data-model.md) |
| JSON Schema contracts | [specs/main/contracts/](contracts/) |

---

## 5. Make targets

| Target | Action |
|--------|--------|
| `make setup` | Install dependencies (uv sync or pip install -e .) |
| `make test` | Build Docker image and run tests inside container |
| `make spec-check` | Verify presence of specs/_meta.md, functional.md, technical.md |

---

## 6. Implementation order (suggested)

1. **001-trend-fetch-mcp** — Trend fetch via MCP; Trend API contract.
2. **006-schema-campaigns-assets** — PostgreSQL schema (campaigns, agents, tasks, video_assets).
3. **002-planner-task-queue** — Planner enqueues Task payloads.
4. **005-worker-task-queue** — Worker pops TaskQueue, runs MCP tools, pushes Result.
5. **003-judge-review-queue** — Judge pops ReviewQueue, OCC, commit or HITL.
6. **004-hitl-queue-dashboard** — HITL queue and dashboard.
7. **007-persona-soul-context** — Load SOUL.md, inject persona into context.
8. **008-openclaw-agent-status** — Publish agent status for discovery.

Before coding any feature, name the spec and plan; write failing tests first (TDD); ensure no direct API calls outside MCP (constitution).
