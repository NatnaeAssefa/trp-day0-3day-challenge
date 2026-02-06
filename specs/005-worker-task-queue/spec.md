# Feature Specification: Worker Service — Pop Tasks, Execute via MCP Tools, Push Result to Review Queue

**Feature Branch**: `005-worker-task-queue`  
**Created**: 2026-02-04  
**Status**: Draft  
**Input**: Implement Worker service that pops tasks from TaskQueue, executes via MCP Tools, and pushes Result with confidence_score to ReviewQueue.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Worker Consumes One Task and Produces One Result (Priority: P1)

As the orchestration system, I need a worker component that takes the next task from the task queue, executes it using only the designated tools (MCP), and pushes a single result payload to the review queue so that the Judge can validate and commit or escalate. Each result MUST include the task identifier, execution status (success or failure), the artifact produced (if any), a confidence score (0.0–1.0), and a timestamp so that the Judge can route and audit correctly.

**Why this priority**: Workers are the execution layer; without them, tasks from the Planner never become results for the Judge.

**Independent Test**: Enqueue a task payload that conforms to the Task contract; run the worker component; verify that exactly one result payload is pushed to the review queue and that the result includes task_id, status, artifact (or null), confidence_score, and created_at, and conforms to the Result contract.

**Acceptance Scenarios**:

1. **Given** at least one task on the task queue, **When** the worker runs, **Then** it pops one task and executes it using only the designated tools (no direct external API calls); on completion it pushes one result to the review queue.
2. **Given** a task that completes successfully, **When** the worker finishes, **Then** the result has status success, an artifact (if the task produces output), a confidence_score in the range 0.0–1.0, task_id matching the task, and created_at set.
3. **Given** a task that fails (e.g. tool error, validation failure), **When** the worker finishes, **Then** the result has status failure, and the worker still pushes a result to the review queue (with artifact null or error details as defined by the contract) so that the Judge can record the failure and the Planner can re-plan if needed.

---

### User Story 2 - Execution Uses Only Designated Tools (MCP) (Priority: P2)

As the system architect, I need the worker to perform all external actions (e.g. generating content, calling APIs, reading resources) only through the designated tool layer (MCP) so that governance, rate limiting, and substitution of backends are enforced in one place and the worker remains decoupled from specific APIs.

**Why this priority**: Project rules require MCP-only external I/O; the worker must not bypass the tool layer.

**Independent Test**: Execute a task that requires an external action; verify that the action is performed via the designated tool interface (e.g. MCP) and that no direct out-of-band calls are made for the same purpose.

**Acceptance Scenarios**:

1. **Given** a task that requires fetching data or calling an external capability, **When** the worker executes, **Then** it uses only the designated tools (MCP) exposed to it; it does not open direct connections or use undocumented endpoints for that capability.
2. **Given** a task that requires multiple steps (e.g. fetch then generate), **When** the worker executes, **Then** each step that touches the external world is performed via the tool layer; the worker may coordinate steps internally but does not bypass the tool layer for external I/O.

---

### User Story 3 - Result Conforms to Contract and Includes Confidence Score (Priority: P3)

As the Judge or a tester, I need every result pushed to the review queue to conform to the published Result payload contract and to include a valid confidence_score so that the Judge can route results (auto-approve, HITL, or reject) without missing or malformed data.

**Why this priority**: Contract compliance and confidence scoring are required for the Judge and HITL flow to work.

**Independent Test**: Run the worker on a set of tasks; for each result on the review queue, assert that the payload has task_id, status, artifact (or null), confidence_score (number in [0, 1]), reasoning_trace (optional), and created_at, and that task_id matches the consumed task.

**Acceptance Scenarios**:

1. **Given** any result produced by the worker, **When** the consumer validates it, **Then** the result has task_id (string), status (success or failure), artifact (object, string, or null), confidence_score (number between 0.0 and 1.0 inclusive), reasoning_trace (optional string), and created_at (timestamp).
2. **Given** a successful execution, **When** the worker produces a result, **Then** the confidence_score reflects the worker’s or model’s estimate of output quality or safety (per project rules); the value is in the allowed range so the Judge can apply threshold rules.
3. **Given** a failed execution, **When** the worker produces a result, **Then** status is failure and confidence_score may be low or zero; the result is still pushed so that the Judge and Planner can react.

---

### Edge Cases

- What happens when the task queue is empty? The worker completes without error and does not push anything to the review queue; it may sleep or poll again according to implementation policy.
- What happens when a task payload is malformed or missing required fields? The worker MUST NOT crash; it MAY push a result with status failure and minimal artifact (e.g. error reason) so that the Judge can record the failure, or it MAY dead-letter the task; the behaviour MUST be defined and consistent.
- What happens when the designated tool (MCP) is unavailable or times out? The worker produces a result with status failure and records the failure reason (in artifact or reasoning_trace as defined); it does not retry indefinitely without bound. The result is pushed to the review queue so the Judge and Planner can react.
- What happens when multiple workers run concurrently? Each worker pops a different task (or the same task is not duplicated to multiple workers) so that each task is executed at most once; task distribution or locking is defined by the queue or orchestration layer.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST provide a worker component that consumes tasks from the designated task queue one at a time and executes each task to completion before consuming the next.
- **FR-002**: For each consumed task, the worker MUST execute it using only the designated tools (MCP) for any external data or actions; it MUST NOT perform direct API calls or out-of-band requests for capabilities that the tools provide.
- **FR-003**: After executing a task, the worker MUST push exactly one result payload to the designated review queue; the result MUST conform to the published Result contract (task_id, status, artifact, confidence_score, reasoning_trace, created_at).
- **FR-004**: The result MUST include a confidence_score in the range 0.0–1.0 so that the Judge can apply routing rules (auto-approve, HITL, reject); the score MUST reflect the worker’s or model’s estimate of output quality or safety per project rules.
- **FR-005**: The result MUST include the task_id of the task that was executed so that the Judge and Planner can correlate results with tasks.
- **FR-006**: On successful execution, the result MUST have status success and MAY include an artifact (e.g. generated text, image reference, transaction id); on failure, the result MUST have status failure and MAY include error details in artifact or reasoning_trace.
- **FR-007**: When the task queue is empty, the worker MUST complete without error and MUST NOT push any result to the review queue.
- **FR-008**: When the worker cannot execute a task (e.g. malformed task, tool unavailable), it MUST produce a result with status failure and push it to the review queue (or handle via a defined dead-letter path) so that the system does not lose track of the task.

### Key Entities

- **Task (payload)**: A unit of work conforming to the Task contract, consumed from the task queue. Contains task_id, task_type, priority, context (goal_description, persona_constraints, required_resources), created_at, status.
- **Task queue**: The designated queue from which the worker pops tasks. Provided by the orchestration layer; this feature consumes from it.
- **Result (payload)**: The output of one task execution, conforming to the Result contract: task_id, status, artifact, confidence_score, reasoning_trace, created_at. Pushed to the review queue.
- **Review queue**: The designated queue to which the worker pushes results. Consumed by the Judge; implementation is out of scope.
- **Designated tools (MCP)**: The tool layer through which the worker performs all external actions (e.g. generate content, call APIs, read resources). The worker must not bypass this layer.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A task placed on the task queue is consumed by a worker and a conforming result appears on the review queue within a defined time (e.g. within 60 seconds for a typical task) so that the pipeline progresses.
- **SC-002**: One hundred percent of results pushed by the worker conform to the Result contract; contract tests can validate worker output without implementation knowledge.
- **SC-003**: Every result includes a valid confidence_score in [0.0, 1.0] so that the Judge can route results correctly; no result is committed or escalated with a missing or invalid score.
- **SC-004**: When the worker executes a task, all external actions are performed via the designated tools (MCP); no direct external calls bypass the tool layer for the same capability.

## Assumptions

- The Task and Result payload contracts are defined in the project technical specification; the worker consumes tasks and produces results in those shapes.
- The task queue and review queue exist and are the designated destinations; connectivity and scaling are outside this feature’s scope.
- The designated tools (MCP) are available and configured for the worker; tool discovery and configuration are defined elsewhere.
- Workers are stateless with respect to each other; each worker instance may process one task at a time (or a defined concurrency limit) so that task distribution is predictable.
- Confidence score may be produced by the worker logic, by a model, or by a separate step; the worker is responsible for attaching a value in the allowed range to each result.
