---
description: "Task list for Project Chimera Core Implementation (features 001–008)"
---

# Tasks: Project Chimera — Core Implementation

**Input**: Design documents from `specs/main/` (plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md)  
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/

**Tests**: Included per constitution (TDD). Write failing tests first; then implement.

**Organization**: Tasks grouped by feature (001→008 per quickstart order). Each feature phase is independently testable.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Feature phase (US1=001, US2=006, US3=002, US4=005, US5=003, US6=004, US7=007, US8=008)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root (per plan.md)
- Contracts: `specs/main/contracts/` (task-payload.json, worker-result-payload.json, trend-api.json)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and structure per plan.md

- [x] T001 Create directory structure src/models, src/services, src/cli, src/lib, tests/contract, tests/integration, tests/unit per specs/main/plan.md
- [x] T002 Ensure pyproject.toml includes pydantic>=2.0, redis>=5.0, mcp>=1.0, pytest, pytest-asyncio per plan Technical Context
- [x] T003 [P] Configure ruff or equivalent lint/format and add make lint target in Makefile

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared models and infra that ALL feature phases depend on. No feature work until this phase is complete.

**Independent Test**: Pydantic models validate against specs/main/contracts/*.json; Redis client can push/pop test payload.

- [x] T004 [P] Add Pydantic model for Task payload in src/models/task.py conforming to specs/main/contracts/task-payload.json and specs/technical.md §1
- [x] T005 [P] Add Pydantic model for WorkerResult payload in src/models/worker_result.py conforming to specs/main/contracts/worker-result-payload.json and specs/technical.md §2
- [x] T006 [P] Add Pydantic model for TrendItem (list response) in src/models/trend.py conforming to specs/main/contracts/trend-api.json and specs/technical.md §3
- [x] T007 Implement Redis queue adapter (push/pop) for TaskQueue and ReviewQueue in src/lib/queue_client.py with env-based connection
- [x] T008 Add environment configuration (e.g. Redis URL, optional DB URL) in src/lib/config.py and document in README or .env.example
- [x] T009 [P] Contract test: validate Task payload shape in tests/contract/test_task_payload.py using specs/main/contracts/task-payload.json

**Checkpoint**: Foundation ready — feature implementation can begin in order 001 → 006 → 002 → 005 → 003 → 004 → 007 → 008

---

## Phase 3: User Story 1 — Fetch trends from MCP (001) — MVP

**Goal**: Consumer can request trends from MCP and receive a list conforming to Trend API contract (id, title, relevance_score, source, timestamp). Spec: specs/001-trend-fetch-mcp/spec.md.

**Independent Test**: Call trend-fetch with valid resource and optional time window; assert response is list and every item has the five required fields and types.

### Tests for 001 (TDD: write first, must fail)

- [x] T010 [P] [US1] Contract test for trend API response shape in tests/contract/test_trend_api.py asserting each item has id, title, relevance_score, source, timestamp per specs/main/contracts/trend-api.json
- [x] T011 [P] [US1] Unit or integration test for trend-fetch skill/service in tests/integration/test_trend_fetch.py (valid resource returns list; empty list when no trends)

### Implementation for 001

- [x] T012 [US1] Implement trend-fetch service or skill in src/services/trend_fetcher.py that obtains data via MCP only and returns list of TrendItem per specs/001-trend-fetch-mcp/spec.md
- [x] T013 [US1] Wire trend-fetcher to MCP resource client (stub or real) in src/services/trend_fetcher.py and ensure response validates with src/models/trend.py
- [x] T014 [US1] Add optional time_range_hours parameter and document in skill README or specs

**Checkpoint**: Trend fetch feature is independently testable; Planner can consume trend data (next phase).

---

## Phase 4: User Story 2 — Schema campaigns, agents, tasks, video_assets (006)

**Goal**: PostgreSQL schema for campaigns, agents, tasks, video_assets per ERD in specs/technical.md §4 and specs/006-schema-campaigns-assets/spec.md. Referential integrity enforced.

**Independent Test**: Apply schema; insert campaign → agent, task → video_asset; query by id and relationship; invalid FKs rejected.

### Tests for 006

- [ ] T015 [P] [US2] Integration test for schema: create campaign, agent, task, video_asset in tests/integration/test_schema_006.py and assert FK constraints and retrievability per data-model.md

### Implementation for 006

- [ ] T016 [US2] Add migration or DDL for campaigns, agents, tasks, video_assets in migrations/ or sql/ per specs/main/data-model.md §2 and specs/technical.md §4
- [ ] T017 [P] [US2] Add Pydantic or ORM models for Campaign, Agent, Task, VideoAsset in src/models/campaign.py, src/models/agent.py, src/models/task_entity.py, src/models/video_asset.py matching ERD
- [ ] T018 [US2] Add repository or DB layer for campaigns/agents/tasks/video_assets in src/services/repository.py (or per-entity) with CRUD needed by Planner/Judge

**Checkpoint**: Schema and persistence layer ready for Planner and Judge to read/write state.

---

## Phase 5: User Story 3 — Planner task queue (002)

**Goal**: Planner reads state/goals, decomposes into tasks, enqueues Task payloads to Redis TaskQueue. Spec: specs/002-planner-task-queue/spec.md.

**Independent Test**: Supply global state and campaign goals; run Planner; verify one or more Task payloads on queue with required fields per Task contract.

### Tests for 002

- [ ] T019 [P] [US3] Contract test: assert Planner output tasks conform to task-payload.json in tests/contract/test_planner_output.py
- [ ] T020 [US3] Integration test: run Planner with mock state and goals in tests/integration/test_planner.py and assert tasks enqueued to TaskQueue

### Implementation for 002

- [ ] T021 [US3] Implement Planner service in src/services/planner.py that reads GlobalState (and campaign goals), decomposes into tasks, uses src/models/task.py and src/lib/queue_client.py to enqueue to TaskQueue per specs/002-planner-task-queue/spec.md
- [ ] T022 [US3] Ensure enqueued task payloads include task_id, task_type, priority, context (goal_description, persona_constraints, required_resources), created_at, status per specs/technical.md §1
- [ ] T023 [US3] Add logic to produce zero tasks when no active goals or no new work in src/services/planner.py

**Checkpoint**: Planner enqueues valid Task payloads; Workers can consume (next phase).

---

## Phase 6: User Story 4 — Worker task queue (005)

**Goal**: Worker pops TaskQueue, runs MCP tools, pushes WorkerResult (with confidence_score) to ReviewQueue. Spec: specs/005-worker-task-queue/spec.md.

**Independent Test**: Enqueue a task; run Worker; verify result on ReviewQueue with task_id, status, confidence_score, artifact/reasoning_trace per contract.

### Tests for 005

- [ ] T024 [P] [US4] Contract test: WorkerResult shape in tests/contract/test_worker_result.py per specs/main/contracts/worker-result-payload.json
- [ ] T025 [US4] Integration test: Worker pops task and pushes result in tests/integration/test_worker.py

### Implementation for 005

- [ ] T026 [US4] Implement Worker service in src/services/worker.py that pops from TaskQueue via src/lib/queue_client.py, executes via MCP tools only, builds WorkerResult using src/models/worker_result.py
- [ ] T027 [US4] Push result to ReviewQueue with confidence_score (0.0–1.0), status success|failure, artifact, reasoning_trace per specs/technical.md §2
- [ ] T028 [US4] Ensure no direct API calls; all external action via MCP in src/services/worker.py

**Checkpoint**: Worker produces Judge-ready results on ReviewQueue.

---

## Phase 7: User Story 5 — Judge review queue (003)

**Goal**: Judge pops ReviewQueue, applies confidence and sensitive-topic rules, commits to GlobalState or escalates to HITL. Spec: specs/003-judge-review-queue/spec.md.

**Independent Test**: Push WorkerResult to ReviewQueue; run Judge; verify high confidence → commit path, low → reject, medium/sensitive → HITL queue.

### Tests for 003

- [ ] T029 [US5] Integration test: Judge routing (commit / reject / HITL) in tests/integration/test_judge.py per research.md HITL rules

### Implementation for 003

- [ ] T030 [US5] Implement Judge service in src/services/judge.py that pops from ReviewQueue via src/lib/queue_client.py
- [ ] T031 [US5] Apply confidence routing: >0.90 auto-approve and commit; 0.70–0.90 send to HITL queue; <0.70 reject and signal Planner per specs/functional.md and research.md
- [ ] T032 [US5] Apply sensitive-topic filter (Politics, Health, Financial, Legal) and route to HITL regardless of confidence in src/services/judge.py
- [ ] T033 [US5] Commit approved results to GlobalState/DB only from Judge (no commit path from Worker) per constitution

**Checkpoint**: Judge is single gatekeeper; HITL queue receives items for Phase 8.

---

## Phase 8: User Story 6 — HITL queue and dashboard (004)

**Goal**: HITL queue and dashboard (or API) for Approve / Reject / Edit on items escalated by Judge. Spec: specs/004-hitl-queue-dashboard/spec.md.

**Independent Test**: Add item to HITL queue; operator Approve/Reject/Edit; state updates and commit path or rejection reflected.

### Implementation for 004

- [ ] T034 [US6] Implement HITL queue consumption and Approve/Reject/Edit actions in src/services/hitl_service.py per specs/004-hitl-queue-dashboard/spec.md
- [ ] T035 [US6] Expose HITL queue listing and action API or CLI in src/cli/hitl.py or src/services/hitl_service.py
- [ ] T036 [US6] On Approve, commit to GlobalState via same path as Judge auto-approve; on Reject, signal Planner or mark task failed
- [ ] T037 [US6] Support Edit then Approve flow and document in specs or README

**Checkpoint**: Full HITL loop operable.

---

## Phase 9: User Story 7 — Persona / SOUL context (007)

**Goal**: Load persona from SOUL.md and inject backstory, voice, directives into context. Spec: specs/007-persona-soul-context/spec.md.

**Independent Test**: Load SOUL.md for an agent; inject into context; downstream (Planner/Worker) receives persona fields.

### Implementation for 007

- [ ] T038 [US7] Implement SOUL loader in src/lib/soul_loader.py that reads SOUL.md and returns structured persona (backstory, voice, directives)
- [ ] T039 [US7] Integrate soul_loader into Planner/Worker context building (e.g. agent context includes persona from soul_md_path) per specs/007-persona-soul-context/spec.md
- [ ] T040 [US7] Document SOUL.md format and injection points in specs or skills README

**Checkpoint**: Persona drives context for agents.

---

## Phase 10: User Story 8 — OpenClaw agent status (008)

**Goal**: Publish agent availability/status to OpenClaw-style network for discovery. Spec: specs/008-openclaw-agent-status/spec.md and specs/openclaw_integration.md.

**Independent Test**: Publish status for an agent; consumer can discover availability.

### Implementation for 008

- [ ] T041 [US8] Implement agent status publisher in src/services/agent_status.py that publishes availability/status per specs/008-openclaw-agent-status/spec.md
- [ ] T042 [US8] Wire publisher to agent lifecycle or heartbeat and document discovery contract in specs/openclaw_integration.md
- [ ] T043 [US8] Ensure no hardcoded secrets; use config for discovery endpoint/credentials per constitution

**Checkpoint**: Agent discovery available for OpenClaw-style integration.

---

## Phase 11: Polish & Cross-Cutting Concerns

**Purpose**: Documentation, validation, and cross-feature quality

- [x] T044 [P] Update README with setup, make targets, and pointer to specs/main/quickstart.md
- [ ] T045 Run full test suite (make test) and fix any regressions; ensure Docker build passes
- [ ] T046 [P] Run quickstart validation: follow specs/main/quickstart.md and confirm make setup, make test, make spec-check succeed
- [ ] T047 Security pass: verify no hardcoded secrets; config via env per constitution
- [ ] T048 Add or update .cursor/rules or agent context if new tech was introduced (or run update-agent-context.ps1)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies — start immediately.
- **Phase 2 (Foundational)**: Depends on Phase 1. **Blocks all feature phases.**
- **Phases 3–10 (Features)**: Depend on Phase 2. Execute in order 001 → 006 → 002 → 005 → 003 → 004 → 007 → 008 per quickstart.md (006 after 001 so schema exists before Planner/Worker/Judge persist).
- **Phase 11 (Polish)**: After all desired feature phases are complete.

### Feature Dependencies

- **US1 (001)**: After Foundational. No other story dependency.
- **US2 (006)**: After Foundational. Needed for US3/US5/US6 (persistence).
- **US3 (002)**: After 001 (trends) and 006 (schema). Planner enqueues tasks.
- **US4 (005)**: After 002. Worker consumes TaskQueue.
- **US5 (003)**: After 005. Judge consumes ReviewQueue.
- **US6 (004)**: After 003. HITL consumes Judge-escalated items.
- **US7 (007)**: After 006 (agents have soul_md_path). Can parallel with 008.
- **US8 (008)**: After agents exist. Can parallel with 007.

### Within Each Feature Phase

- Tests (TDD) written first and must fail before implementation.
- Models/contracts before services; services before integration.
- Commit after each task or logical group.

### Parallel Opportunities

- Phase 1: T003 [P] can run in parallel with T001–T002.
- Phase 2: T004, T005, T006, T009 [P] (models + one contract test) can run in parallel; T007, T008 sequential after.
- Within a phase: tasks marked [P] (e.g. contract tests, multiple model files) can run in parallel.
- US7 and US8 can be worked in parallel after US6.

---

## Parallel Example: Phase 2 (Foundational)

```bash
# Parallel: all payload models and one contract test
Task T004: "Add Pydantic model for Task payload in src/models/task.py ..."
Task T005: "Add Pydantic model for WorkerResult payload in src/models/worker_result.py ..."
Task T006: "Add Pydantic model for TrendItem in src/models/trend.py ..."
Task T009: "Contract test: validate Task payload shape in tests/contract/test_task_payload.py ..."
# Then sequential: T007 queue client, T008 config
```

---

## Implementation Strategy

### MVP First (001 + Foundation)

1. Complete Phase 1: Setup  
2. Complete Phase 2: Foundational  
3. Complete Phase 3: User Story 1 (001 Trend fetch)  
4. **STOP and VALIDATE**: Run contract and integration tests for 001; trend list conforms to Trend API  
5. Demo: consumer can request trends via MCP and get contract-compliant list  

### Incremental Delivery

1. Setup + Foundational → shared models and queues ready  
2. 001 → Trend fetch (MVP)  
3. 006 → Schema and persistence  
4. 002 → Planner enqueues tasks  
5. 005 → Worker produces results  
6. 003 → Judge routes commit/reject/HITL  
7. 004 → HITL queue and actions  
8. 007 → Persona from SOUL  
9. 008 → OpenClaw status  
10. Polish → Docs, security, quickstart validation  

### Traceability

- Every task references specs (e.g. specs/001-trend-fetch-mcp/spec.md) or contracts (specs/main/contracts/).  
- Tests assert against specs/technical.md and JSON contracts.  
- Constitution: TDD (tests first), MCP-only I/O, Judge as gatekeeper, traceability.

---

## Notes

- [P] = parallelizable (different files / no blocking deps).  
- [USn] = feature phase for traceability.  
- Each feature phase is independently testable.  
- Verify tests fail before implementing (TDD).  
- Commit after each task or logical group.  
- No direct API calls outside MCP (constitution).
