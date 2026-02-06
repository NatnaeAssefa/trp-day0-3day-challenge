# Feature Specification: Planner Service — Read Goals, Decompose into Tasks, Enqueue

**Feature Branch**: `002-planner-task-queue`  
**Created**: 2026-02-04  
**Status**: Draft  
**Input**: Implement Planner service that reads GlobalState and campaign goals, decomposes goals into tasks, and pushes Task payloads to Redis TaskQueue.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Planning Component Produces Tasks from Goals (Priority: P1)

As the orchestration system, I need a planning component that reads the current global state and active campaign goals, decomposes those goals into discrete, executable tasks, and enqueues each task to the task queue so that workers can pick them up and execute them. Each enqueued item must conform to the published Task payload contract (unique task id, task type, priority, context with goal description and constraints, status, and timestamp) so that workers and the judge can process tasks consistently.

**Why this priority**: The Planner is the entry point for turning operator intent (goals) into work; without it, no tasks reach the queue and the swarm cannot operate.

**Independent Test**: Supply a defined global state and a set of campaign goals; run the planning component; verify that one or more task payloads appear on the task queue and that each payload contains all required fields and allowed values per the Task contract.

**Acceptance Scenarios**:

1. **Given** global state and at least one campaign goal, **When** the planning component runs, **Then** at least one task payload is enqueued to the task queue and each payload includes task_id, task_type, priority, context (goal_description, persona_constraints, required_resources), created_at, and status set to pending (or equivalent initial status).
2. **Given** a goal that implies multiple actions (e.g. "reply to 10 comments"), **When** the planning component runs, **Then** multiple task payloads are enqueued so that each actionable unit is a separate task.
3. **Given** global state with no active goals or goals that require no new work, **When** the planning component runs, **Then** either zero tasks are enqueued or the component completes without error and does not enqueue invalid or duplicate tasks.

---

### User Story 2 - Tasks Conform to Contract for Downstream Consumers (Priority: P2)

As a Worker or system validator, I need every task taken from the task queue to conform to the published Task payload contract so that I can safely parse, execute, and track tasks without handling multiple shapes or missing fields.

**Why this priority**: Contract compliance ensures the Worker and Judge can rely on a stable task shape; it also enables contract tests to validate the Planner output.

**Independent Test**: After the planning component runs, inspect each enqueued task payload and assert that it satisfies the Task contract (required fields, allowed enum values, and types as defined in the project technical specification).

**Acceptance Scenarios**:

1. **Given** any task payload produced by the planning component, **When** the consumer validates it, **Then** the payload has task_id (string, unique), task_type (one of the allowed types), priority (one of the allowed levels), context (object with goal_description, persona_constraints, required_resources), created_at (timestamp), and status (one of the allowed statuses).
2. **Given** required_resources in context, **When** present, **Then** each entry is a valid resource identifier (e.g. URI form) so that workers know which resources to use.

---

### User Story 3 - Planning Reacts to State and Goals (Priority: P3)

As an operator, I need the planning component to use the current global state (e.g. campaign progress, budget, recent outcomes) and the active campaign goals when decomposing so that tasks are relevant and not duplicated or obsolete.

**Why this priority**: Ensures the Planner is not stateless; it respects what has already been done and what the goals require.

**Independent Test**: Run the planning component with different global state snapshots (e.g. different progress or paused campaign) and verify that the number or content of enqueued tasks differs appropriately (e.g. no tasks when campaign is paused, or fewer tasks when some work is already done).

**Acceptance Scenarios**:

1. **Given** global state indicating the campaign is paused or has no active goals, **When** the planning component runs, **Then** it does not enqueue new tasks (or enqueues only tasks that are explicitly allowed in that state).
2. **Given** global state that reflects recent task completions, **When** the planning component runs, **Then** it does not enqueue duplicate tasks for the same logical work; decomposition is idempotent or state-aware.

---

### Edge Cases

- What happens when the task queue is temporarily full or unavailable? The system MUST handle this without losing task definitions; either retry with backoff, persist tasks for later enqueue, or surface a defined error so that the operator or orchestrator can react. The exact strategy is implementation-defined but MUST be consistent and observable.
- What happens when goal description is ambiguous or very large? The planning component MUST produce at least one task or a defined "no-op" outcome (e.g. zero tasks) and MUST NOT enqueue malformed or contract-invalid payloads.
- What happens when global state is missing or partially available? The system MUST use a safe default (e.g. empty or read-only snapshot) so that the Planner can still run and either produce no tasks or a minimal safe set, rather than failing in an undefined way.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST provide a planning component that reads global state and campaign goals from the designated sources and produces one or more task definitions.
- **FR-002**: Each task definition MUST conform to the published Task payload contract (task_id, task_type, priority, context, created_at, status and any other required fields as defined in the project technical specification).
- **FR-003**: The system MUST enqueue each produced task to the designated task queue so that workers can consume them; enqueue order or prioritization MAY be defined by the contract or configuration.
- **FR-004**: The planning component MUST use only the current global state and active campaign goals as input for decomposition; it MUST NOT invent goals or ignore paused or inactive campaigns when so indicated by state.
- **FR-005**: When decomposition yields zero tasks (e.g. no goals or no new work), the component MUST complete without error and MUST NOT enqueue placeholder or invalid tasks.
- **FR-006**: The system MUST ensure each enqueued task has a unique task_id so that workers and the judge can track and deduplicate work.

### Key Entities

- **Global state**: The current view of the system used by the Planner (e.g. campaign progress, budget, recent outcomes, queue depths). Read by the planning component; not owned by this feature.
- **Campaign goal**: A high-level objective (e.g. "promote product X to audience Y") that the Planner decomposes into tasks. Source and format are defined elsewhere; this feature consumes goals.
- **Task (payload)**: A single unit of work conforming to the Task contract: unique id, type, priority, context (goal description, persona constraints, required resources), timestamp, status. Produced by the Planner and enqueued for Workers.
- **Task queue**: The designated queue where task payloads are placed for worker consumption. This feature enqueues to it; queue implementation and topology are out of scope of this spec.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Operators can set campaign goals and run the planning component; within a defined time window (e.g. under 60 seconds for a typical batch), tasks appear on the task queue and workers can consume them.
- **SC-002**: One hundred percent of enqueued task payloads conform to the Task contract; contract tests can validate Planner output without implementation knowledge.
- **SC-003**: When global state indicates no active goals or a paused campaign, the planning component produces zero new tasks and completes without failure.
- **SC-004**: The system supports at least one active campaign and multiple goals without conflating or dropping tasks; task count and content reflect the goals and state in a predictable way.

## Assumptions

- Global state and campaign goals are available from a defined source (e.g. store, API, or file) that this feature can read; the format and update frequency are defined elsewhere.
- The Task payload contract is defined in the project technical specification; the Planner MUST produce payloads that satisfy that contract.
- The task queue exists and is the designated destination for task payloads; connectivity, durability, and scaling of the queue are outside this feature’s scope.
- "Decompose" means translating one or more goals into one or more task definitions; the exact decomposition strategy (e.g. rule-based vs. model-based) is an implementation choice as long as the output conforms to the contract and respects state and goals.
