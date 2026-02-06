# Feature Specification: Judge Service — Pop Results, Validate (OCC), Commit or Escalate to HITL

**Feature Branch**: `003-judge-review-queue`  
**Created**: 2026-02-04  
**Status**: Draft  
**Input**: Implement Judge service that pops results from ReviewQueue, validates with OCC, and commits to GlobalState or escalates to HITL queue.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Judge Consumes Results and Decides Commit or Escalate (Priority: P1)

As the orchestration system, I need a judge component that takes the next result from the review queue, validates it (including an optimistic concurrency check against the current global state), and then either commits the result to global state so that downstream steps can proceed, or escalates the result to the human-in-the-loop (HITL) queue so that a human can approve, reject, or edit before any commit. The judge MUST be the only component that can commit worker results to global state so that quality and safety are enforced in one place.

**Why this priority**: The Judge is the gatekeeper for all worker output; without it, results are not validated and either never reach global state or bypass safety checks.

**Independent Test**: Enqueue a result payload that conforms to the Result contract; run the judge component; verify that the result is either committed (and visible in global state or its effects) or placed on the HITL queue, and that no result is both committed and escalated.

**Acceptance Scenarios**:

1. **Given** at least one result on the review queue, **When** the judge runs, **Then** it pops one result and processes it: the result is either committed to global state or escalated to the HITL queue (or rejected and re-queued for the planner, per project rules).
2. **Given** a result with a confidence score above the auto-approve threshold and passing validation, **When** the judge runs, **Then** the result is committed to global state and not placed on the HITL queue.
3. **Given** a result with a confidence score in the medium band or triggering a sensitive-topic filter, **When** the judge runs, **Then** the result is placed on the HITL queue and not committed until a human acts (or a defined override applies).

---

### User Story 2 - Optimistic Concurrency Control (OCC) (Priority: P2)

As the system, I need the judge to perform an optimistic concurrency check before committing: if the global state has changed in a relevant way since the worker started the task (e.g. campaign paused, goal cancelled, state version advanced), the judge MUST NOT commit the result and MUST invalidate it and signal the planner to re-plan or re-queue so that no worker output is applied against stale state.

**Why this priority**: OCC prevents race conditions and "ghost updates" when multiple agents or events update state concurrently; it is required by the project architecture.

**Independent Test**: Supply a result that was produced when global state had version V1; when the judge runs, provide global state at version V2 (e.g. campaign paused). Verify the judge does not commit and that the result is invalidated and the planner is signalled (or the result re-queued for re-planning).

**Acceptance Scenarios**:

1. **Given** a result and the current global state, **When** the judge runs the OCC check, **Then** it compares the state version (or equivalent) that the task was based on with the current state; if they differ in a way that invalidates the result, the judge MUST NOT commit.
2. **Given** an OCC failure, **When** the judge completes, **Then** the result is not written to global state and the system signals the planner to re-evaluate (e.g. re-queue the task or re-plan) so that work can be retried against fresh state.
3. **Given** an OCC success (state unchanged or change irrelevant), **When** the judge runs, **Then** it may proceed to commit if all other validation rules pass.

---

### User Story 3 - Results Conform to Contract and Routing Rules (Priority: P3)

As a system integrator or tester, I need every result consumed from the review queue to conform to the published Result payload contract (task_id, status, artifact, confidence_score, reasoning_trace, created_at) and I need the judge to apply the project’s routing rules (e.g. confidence bands and sensitive-topic filters) so that behaviour is predictable and auditable.

**Why this priority**: Contract compliance and explicit routing rules ensure the Judge can be tested and that HITL escalation is consistent.

**Independent Test**: Provide results with different confidence scores and topic flags; verify that the judge routes them according to the documented rules (auto-approve, async HITL, reject/retry, or mandatory HITL for sensitive topics).

**Acceptance Scenarios**:

1. **Given** a result payload, **When** the judge pops it, **Then** the judge treats it as conforming to the Result contract; if a payload is malformed or missing required fields, the judge handles it without committing (e.g. discard or dead-letter) and does not crash.
2. **Given** the project’s confidence thresholds (e.g. high / medium / low bands), **When** the judge evaluates a result, **Then** it routes to commit, to HITL queue, or to reject/retry according to those thresholds.
3. **Given** content that triggers a sensitive-topic filter (e.g. politics, health, financial, legal), **When** the judge evaluates the result, **Then** the result is always sent to the HITL queue for mandatory human review, regardless of confidence score.

---

### Edge Cases

- What happens when the review queue is empty? The judge completes without error and does not modify global state or the HITL queue; it may sleep or poll again according to implementation policy.
- What happens when global state is temporarily unavailable for the OCC check? The judge MUST NOT commit; it MAY retry the check, re-queue the result for later processing, or escalate to HITL so that no commit occurs without a valid OCC check.
- What happens when the HITL queue is full or unavailable? The system MUST retain the result (e.g. leave it in a pending state or re-queue to the review queue) and MUST NOT commit results that should have been escalated; a defined error or backpressure behaviour applies.
- What happens when the same result is processed twice (e.g. duplicate pop or retry)? The system MUST be idempotent or deduplicated by task_id so that a single worker result is not committed twice or double-escalated.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST provide a judge component that consumes results from the designated review queue one at a time and processes each result to completion before taking the next.
- **FR-002**: Each consumed result MUST be treated as conforming to the published Result payload contract (task_id, status, artifact, confidence_score, reasoning_trace, created_at); malformed payloads MUST NOT be committed and MUST be handled in a defined way (e.g. discard or dead-letter).
- **FR-003**: Before committing any result to global state, the judge MUST perform an optimistic concurrency check: if the global state has changed in a way that invalidates the result (e.g. state version or campaign status), the judge MUST NOT commit and MUST invalidate the result and signal the planner to re-plan or re-queue.
- **FR-004**: The judge MUST be the only component that can write worker results into global state; all commit paths go through the judge.
- **FR-005**: The judge MUST route each result according to the project’s rules: e.g. high confidence → commit; medium confidence → HITL queue; low confidence → reject and signal planner; sensitive-topic content → HITL queue regardless of confidence.
- **FR-006**: When the judge escalates a result to the HITL queue, it MUST NOT also commit that result to global state; the result remains pending until a human (or defined override) approves or rejects.
- **FR-007**: When the review queue is empty, the judge MUST complete without error and without modifying global state or the HITL queue.

### Key Entities

- **Result (payload)**: A worker output conforming to the Result contract: task_id, status, artifact, confidence_score, reasoning_trace, created_at. Consumed from the review queue by the judge.
- **Review queue**: The designated queue from which the judge pops results. Implementation and topology are out of scope; this feature consumes from it.
- **Global state**: The shared state updated when the judge commits a result (e.g. campaign progress, task status, artifacts). The judge reads it for OCC and writes to it on commit.
- **HITL queue**: The queue or store where results awaiting human review are placed. The judge enqueues or writes to it when routing requires human approval.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Results that pass validation and OCC are committed to global state within a defined time (e.g. within 30 seconds of being popped) so that the system progresses without unnecessary delay.
- **SC-002**: One hundred percent of commits are preceded by a successful OCC check; no result is committed when the associated state has been invalidated.
- **SC-003**: Results that require human review appear on the HITL queue and are not committed until explicitly approved; routing matches the documented confidence and sensitive-topic rules.
- **SC-004**: Contract tests can validate that the judge only commits results that conform to the Result contract and that routing behaviour is consistent and auditable.

## Assumptions

- The Result payload contract is defined in the project technical specification; the judge consumes payloads that Workers produce in that shape.
- The review queue and HITL queue (or equivalent) exist and are the designated destinations; connectivity and scaling are outside this feature’s scope.
- Global state supports a version or equivalent mechanism so that the judge can perform an OCC check; the exact format is defined elsewhere.
- Confidence thresholds and sensitive-topic definitions are configured or defined in the project’s functional specification; the judge applies them without defining the thresholds in this spec.
- "Escalate to HITL queue" means the result is placed in a queue or store that the human review workflow consumes; the judge does not perform the human approval itself.
