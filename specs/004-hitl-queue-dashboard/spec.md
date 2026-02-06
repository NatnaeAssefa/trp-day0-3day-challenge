# Feature Specification: HITL Queue and Dashboard for Human Approve/Reject/Edit

**Feature Branch**: `004-hitl-queue-dashboard`  
**Created**: 2026-02-04  
**Status**: Draft  
**Input**: Add HITL queue and dashboard so medium-confidence and sensitive-topic results get human Approve/Reject/Edit before commit.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Reviewer Sees Pending Results and Takes Action (Priority: P1)

As a human reviewer, I need a single place (dashboard) where I can see all results that are waiting for my decision—those that were routed because of medium confidence or sensitive topics—and I need to be able to Approve, Reject, or Edit each one so that the system only commits or discards work after I have made an explicit choice. Until I act, the result MUST NOT be committed to global state.

**Why this priority**: The HITL queue and dashboard are the human-facing surface for the safety layer; without them, medium-confidence and sensitive-topic results have no defined path to approval.

**Independent Test**: Route a result to the HITL queue (e.g. simulate Judge escalation); open the dashboard; verify the result appears as pending; perform Approve (or Reject or Edit); verify the system commits only when Approve is used and does not commit when Reject is used, and that Edit allows correction before approval.

**Acceptance Scenarios**:

1. **Given** one or more results have been placed on the HITL queue by the Judge, **When** the reviewer opens the dashboard, **Then** each pending result is visible with enough context (e.g. task id, generated content or artifact summary, confidence score, reason for escalation) to make a decision.
2. **Given** a pending result on the dashboard, **When** the reviewer clicks Approve, **Then** the system records the approval and the result is committed to global state (or handed off to the component that commits), and the item is removed from the pending list.
3. **Given** a pending result, **When** the reviewer clicks Reject, **Then** the system records the rejection and the result is NOT committed; the item is removed from the pending list and the planner may be signalled to retry or drop (per project rules).
4. **Given** a pending result, **When** the reviewer chooses Edit, **Then** the reviewer can modify the content or artifact (within defined limits); after saving edits, the reviewer can then Approve the edited version so that the system commits the revised result, not the original.

---

### User Story 2 - Only Escalated Results Appear on the Queue and Dashboard (Priority: P2)

As the system, I need the HITL queue to receive only results that the Judge has escalated—i.e. those in the medium-confidence band or those that triggered a sensitive-topic filter—so that reviewers are not overwhelmed and the queue reflects the documented routing rules.

**Why this priority**: Correct routing ensures that the queue and dashboard are the single place for "needs human decision" items and that high-confidence auto-approved results never appear there.

**Independent Test**: Send results with high confidence and no sensitive topic; verify they do not appear on the HITL queue or dashboard. Send results with medium confidence or a sensitive topic; verify they do appear and remain until the reviewer acts.

**Acceptance Scenarios**:

1. **Given** a result that the Judge routes to the HITL queue (medium confidence or sensitive topic), **When** the Judge completes processing, **Then** the result is added to the HITL queue and becomes visible on the dashboard for reviewers.
2. **Given** a result that the Judge auto-approves (high confidence, no sensitive topic), **When** the Judge completes processing, **Then** the result is NOT added to the HITL queue and does not appear on the dashboard.
3. **Given** multiple pending items on the queue, **When** the reviewer works through them, **Then** the order or prioritization (e.g. by time, by sensitivity) is consistent and visible so that reviewers can triage effectively.

---

### User Story 3 - Clear Outcome for Each Pending Item (Priority: P3)

As a reviewer or operator, I need each pending item to have a clear, auditable outcome (Approved, Rejected, or Edited-then-Approved) and I need the dashboard to reflect the current state so that nothing is left in limbo and decisions can be traced.

**Why this priority**: Auditability and clear state prevent duplicate reviews and support compliance and debugging.

**Independent Test**: Approve, Reject, and Edit-then-Approve different items; verify that each item shows a final state and that the system does not allow committing without an explicit Approve (or equivalent) action.

**Acceptance Scenarios**:

1. **Given** a pending result, **When** the reviewer takes any action (Approve, Reject, or Edit then Approve/Reject), **Then** the item is removed from the pending list and its outcome is recorded (e.g. approved, rejected, edited-and-approved).
2. **Given** the need to trace past decisions, **When** an operator or auditor queries completed HITL items, **Then** they can see which result was approved, rejected, or edited and when, and by whom if the system supports identity.
3. **Given** an Edit action, **When** the reviewer saves edits, **Then** the system treats the edited version as the candidate for commit on Approve; the original unedited content is not committed.

---

### Edge Cases

- What happens when no reviewers are available? Items remain on the HITL queue and dashboard until a human acts; the system does not auto-commit them. Optional: escalation or alerts can be defined elsewhere.
- What happens when the same result is escalated twice (e.g. duplicate routing)? The system SHOULD deduplicate by task_id or result id so that the reviewer sees one entry per result and does not approve or reject the same result twice.
- What happens when the reviewer closes the dashboard without acting? The item remains pending; no commit occurs. The reviewer can return later to complete the action.
- What happens when the dashboard or queue is temporarily unavailable? Results already on the queue remain; the Judge or upstream component MUST NOT commit results that should have been escalated, and SHOULD retry or retain them until the queue is available.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST provide an HITL queue (or equivalent store) that holds results that require human review—specifically those routed due to medium confidence or sensitive-topic filters—and only those results.
- **FR-002**: The system MUST provide a dashboard (or equivalent interface) that displays all pending items from the HITL queue so that reviewers can see what needs a decision.
- **FR-003**: For each pending item, the dashboard MUST display enough context for the reviewer to decide: at least the task identifier, the generated content or artifact (or a summary), the confidence score, and the reason for escalation (e.g. medium confidence, sensitive topic).
- **FR-004**: The reviewer MUST be able to take exactly three actions per item: **Approve** (result is then committed to global state), **Reject** (result is not committed and may trigger planner retry or drop), **Edit** (reviewer modifies content, then can Approve or Reject the edited version).
- **FR-005**: A result MUST NOT be committed to global state until the reviewer has explicitly approved it (or approved an edited version); Reject MUST prevent commit.
- **FR-006**: When the reviewer Approves (or Approves after Edit), the system MUST record the approval and commit the result (or edited result) through the designated path and MUST remove the item from the pending list.
- **FR-007**: When the reviewer Rejects, the system MUST record the rejection, MUST NOT commit, and MUST remove the item from the pending list; the planner or orchestrator may be notified per project rules.
- **FR-008**: The system MUST support at least one concurrent reviewer viewing and acting on the dashboard; multiple reviewers MAY see the same queue with appropriate assignment or locking so that each item is acted on once.

### Key Entities

- **HITL queue**: The store or queue that holds results awaiting human review. Populated by the Judge when routing rules require human review; consumed by the dashboard and review workflow.
- **Pending item**: A single result on the HITL queue, with associated context (task id, content/artifact, confidence score, escalation reason). Becomes "completed" when the reviewer Approves, Rejects, or Edits-then-Approve/Reject.
- **Dashboard**: The interface (e.g. screen or view) where reviewers see pending items and perform Approve, Reject, or Edit actions.
- **Reviewer**: The human (or role) who uses the dashboard to approve, reject, or edit results. Identity may be recorded for audit.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Reviewers can open the dashboard and see all pending HITL items within a defined time (e.g. within 10 seconds of load) so that they can start work without delay.
- **SC-002**: One hundred percent of results that are routed to the HITL queue appear on the dashboard and remain pending until the reviewer takes an action; no escalated result is committed without explicit Approve.
- **SC-003**: Each Approve, Reject, or Edit action is recorded and reflected in the system state (commit, no-commit, or edited-then-commit) so that operators can trace decisions and outcomes.
- **SC-004**: Reviewers can complete an action (Approve, Reject, or Edit then Approve/Reject) per item in a reasonable time (e.g. under 2 minutes per item when content is visible) so that the queue does not grow unbounded under normal load.

## Assumptions

- The Judge (or equivalent component) is responsible for routing results to the HITL queue; this feature provides the queue and dashboard and the actions Approve/Reject/Edit, and does not define the Judge’s routing logic.
- "Commit to global state" is performed by an existing component (e.g. Judge or orchestrator) when the reviewer approves; this feature records the approval and triggers or hands off to that component.
- Medium-confidence and sensitive-topic definitions are configured or specified elsewhere; this feature assumes items on the HITL queue have already been correctly routed.
- The dashboard may be a simple list or table; advanced UX (e.g. filters, bulk actions) is out of scope unless explicitly added later.
- One reviewer acting on one item at a time is the minimum; multi-reviewer or assignment rules may be added in a later feature.
