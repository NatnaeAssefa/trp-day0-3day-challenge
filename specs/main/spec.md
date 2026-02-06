# Feature Specification: Project Chimera — Core Implementation Plan

**Feature Branch**: `main`  
**Created**: 2026-02-04  
**Status**: Draft  
**Input**: Umbrella implementation plan for the first wave of Project Chimera features. Scope is derived from [specs/_meta.md](../_meta.md), [specs/functional.md](../functional.md), [specs/technical.md](../technical.md), and the ratified feature specs under `specs/001-*` through `specs/008-*`.

## Scope

This spec defines the **implementation plan scope** for the Chimera core: the Planner–Worker–Judge swarm, MCP-only I/O, HITL at the Judge, and supporting data and persona. It does not replace individual feature specs; it aggregates them for planning and design artifacts (research, data model, contracts, quickstart).

### In-scope features (referenced specs)

| # | Feature | Spec path |
|---|---------|-----------|
| 001 | Fetch trends from MCP | [001-trend-fetch-mcp/spec.md](../001-trend-fetch-mcp/spec.md) |
| 002 | Planner task queue | [002-planner-task-queue/spec.md](../002-planner-task-queue/spec.md) |
| 003 | Judge review queue | [003-judge-review-queue/spec.md](../003-judge-review-queue/spec.md) |
| 004 | HITL queue & dashboard | [004-hitl-queue-dashboard/spec.md](../004-hitl-queue-dashboard/spec.md) |
| 005 | Worker task queue | [005-worker-task-queue/spec.md](../005-worker-task-queue/spec.md) |
| 006 | Schema: campaigns, agents, tasks, video_assets | [006-schema-campaigns-assets/spec.md](../006-schema-campaigns-assets/spec.md) |
| 007 | Persona / SOUL context | [007-persona-soul-context/spec.md](../007-persona-soul-context/spec.md) |
| 008 | OpenClaw agent status | [008-openclaw-agent-status/spec.md](../008-openclaw-agent-status/spec.md) |

### Primary requirement

Implement the core Chimera swarm and supporting infrastructure so that:

1. **Perception**: Trends are fetched via MCP and conform to the Trend API contract.
2. **Planning**: The Planner reads state/goals, decomposes into tasks, and enqueues Task payloads (per technical.md §1).
3. **Execution**: Workers pop the task queue, run MCP tools, and push Results with confidence_score to the review queue.
4. **Gatekeeping**: The Judge pops the review queue, applies OCC and confidence/sensitive-topic rules, and either commits to GlobalState or escalates to HITL.
5. **HITL**: A queue and dashboard support Approve / Reject / Edit for items escalated by the Judge.
6. **Persistence**: PostgreSQL holds campaigns, agents, tasks, and video_assets per the ERD in technical.md §4.
7. **Persona**: Persona is loaded from SOUL.md and injected (backstory, voice, directives) into context.
8. **Discovery**: Agent availability/status is publishable to an OpenClaw-style network.

### Technical approach (from research and constitution)

- **Spec-driven**: All behaviour is specified in specs/; implementation and tests reference spec documents and contracts.
- **MCP-only**: External I/O (APIs, data sources) is via MCP; no direct API calls in agent core.
- **TDD**: Tests for contracts/skills are written first and must fail before implementation.
- **Judge as gatekeeper**: Worker outputs and HITL flows go through the Judge only.
- **Traceability**: Plan and tasks reference the spec(s) and contracts being implemented.

## Success criteria

- Design artifacts (research.md, data-model.md, contracts/, quickstart.md) are generated under `specs/main/` and are consistent with the constitution and technical spec.
- Agent context (e.g. Cursor) is updated with the technology stack from the plan.
- Implementation can proceed feature-by-feature (001 → 008) using the same contracts and data model.
