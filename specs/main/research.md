# Research — Project Chimera Core Implementation

**Branch**: `main`  
**Phase**: 0 (Outline & Research)  
**Input**: Technical Context from [plan.md](plan.md); constitution; [research/architecture_strategy.md](../../research/architecture_strategy.md).

This document consolidates research decisions and resolves any "NEEDS CLARIFICATION" from the plan. All items below are already decided in the project; this file records them for traceability and handoff.

---

## 1. Agent orchestration pattern

- **Decision:** Hierarchical swarm (FastRender): Planner → TaskQueue → Workers → ReviewQueue → Judge → GlobalState.
- **Rationale:** SRS §3.1 defines Planner (strategist), Worker (executor), Judge (gatekeeper). Parallel Workers, single Judge for quality and HITL; Planner does decomposition and OCC.
- **Alternatives considered:** Sequential chain (rejected — no parallelism); flat swarm (rejected — no single gatekeeper for HITL and commit).

---

## 2. External I/O (MCP-only)

- **Decision:** All perception (Resources), action (Tools), and prompts for external systems go through the Model Context Protocol (MCP). No direct API calls from agent core.
- **Rationale:** Constitution II; SRS §3.2. Decouples agent logic from platform volatility; MCP servers absorb API changes.
- **Alternatives considered:** Direct API calls from Planner/Worker (rejected — violates constitution and SRS).

---

## 3. Human-in-the-loop (HITL)

- **Decision:** HITL at the Judge layer only. Confidence-based routing: >0.90 auto-approve; 0.70–0.90 async approval (dashboard queue); <0.70 reject and signal Planner. Sensitive-topic filters always route to HITL.
- **Rationale:** Constitution IV; SRS §5.1; single enforcement point for safety and audit.
- **Alternatives considered:** HITL inside Worker or Planner (rejected — constitution requires Judge as gatekeeper).

---

## 4. Storage and queues

- **Decision:** PostgreSQL for campaigns, agents, tasks, video_assets (transactional and high-velocity metadata). Redis for TaskQueue, ReviewQueue, episodic cache. Weaviate for semantic memory (reference; not in scope for this plan’s implementation tasks).
- **Rationale:** research/architecture_strategy.md §3; SRS §2.3. Relational integrity and JSONB for flexible metadata; Redis for low-latency queues.
- **Alternatives considered:** NoSQL for video metadata (rejected — consistency and schema discipline better in PostgreSQL).

---

## 5. Testing and tooling

- **Decision:** pytest and pytest-asyncio; contract tests for API shapes (Task, Worker Result, Trend API); skill I/O tests per skills/*/README.md. Tests must fail before implementation (TDD).
- **Rationale:** Constitution III; pyproject.toml; specs/technical.md contracts.
- **Alternatives considered:** Implementation-first tests (rejected — constitution requires TDD).

---

## 6. Traceability

- **Decision:** Plan and tasks reference spec(s) and contracts by name. Tests assert against specs/technical.md and skill READMEs. No implementation without a ratified spec.
- **Rationale:** Constitution I and V; reduces scope creep and unspecified behaviour.

---

**Status:** All Technical Context items from plan.md are resolved. No NEEDS CLARIFICATION remaining. Phase 1 (design and contracts) can proceed.
