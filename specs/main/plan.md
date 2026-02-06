# Implementation Plan: Project Chimera — Core Implementation

**Branch**: `main` | **Date**: 2026-02-04 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `specs/main/spec.md` (umbrella scope for features 001–008)

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement the core Chimera swarm (Planner–Worker–Judge) and supporting infrastructure: trend fetch via MCP (001), Planner task queue (002), Judge review queue (003), HITL queue and dashboard (004), Worker task queue (005), PostgreSQL schema for campaigns/agents/tasks/video_assets (006), persona from SOUL.md (007), and OpenClaw-style agent status (008). All behaviour is spec-driven; external I/O is MCP-only; Judge is the single gatekeeper; TDD and traceability apply per constitution.

## Technical Context

**Language/Version**: Python 3.11+  
**Primary Dependencies**: pydantic >= 2.0, redis >= 5.0, mcp >= 1.0 (per pyproject.toml)  
**Storage**: PostgreSQL (campaigns, agents, tasks, video_assets); Redis (queues); Weaviate (semantic memory — reference only in this plan)  
**Testing**: pytest, pytest-asyncio; contract and unit tests under `tests/`  
**Target Platform**: Linux server (Docker); CI via GitHub Actions  
**Project Type**: single (backend/service)  
**Performance Goals**: Trend response under ~30s for typical batch; queue throughput sufficient for async Planner/Worker/Judge flow  
**Constraints**: MCP-only external I/O; no hardcoded secrets; Judge-only commit path to GlobalState  
**Scale/Scope**: First wave = 8 feature specs (001–008); single Chimera deployment

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Verify compliance with `.specify/memory/constitution.md`:

- **Spec-Driven:** Feature scope is specified or will be added to `specs/` before implementation.
- **MCP-Only:** External I/O (APIs, data sources) is via MCP; no direct API calls in agent core.
- **TDD:** Tests for new contracts/skills are planned and will fail before implementation.
- **Judge as Gatekeeper:** Any new Worker outputs or HITL flows are designed to go through the Judge.
- **Traceability:** Plan and tasks reference the spec(s) and contracts being implemented.

## Project Structure

### Documentation (this feature)

```text
specs/main/
├── plan.md              # This file (/speckit.plan command output)
├── spec.md              # Umbrella feature spec (scope 001–008)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
research/
├── architecture_strategy.md
└── tooling_strategy.md

specs/
├── _meta.md
├── functional.md
├── technical.md
├── main/                # This plan
├── 001-trend-fetch-mcp/ … 008-openclaw-agent-status/

skills/                 # Runtime capability packages (I/O in READMEs)
tests/
├── contract/
├── integration/
└── unit/

# Target layout for implementation (src/ as feature work proceeds)
src/
├── models/
├── services/
├── cli/
└── lib/
```

**Structure Decision**: Single project. Current layout has `tests/`, `research/`, `specs/`, `skills/`. Implementation will add `src/` (models, services, cli, lib) as features 001–008 are implemented. Contracts and data model are defined in `specs/technical.md` and `specs/main/contracts/`.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations. All constitution gates pass; this plan does not introduce exceptions.
