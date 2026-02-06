# Feature Specification: Persistent Schema for Campaigns, Agents, Tasks, and Video Assets

**Feature Branch**: `006-schema-campaigns-assets`  
**Created**: 2026-02-04  
**Status**: Draft  
**Input**: Add PostgreSQL schema for campaigns, agents, tasks, and video_assets per specs/technical.md ERD.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - System Can Persist and Query Campaigns, Agents, Tasks, and Video Assets (Priority: P1)

As the orchestration system, I need a persistent schema that stores campaigns, agents, tasks, and video assets with the attributes and relationships defined in the project’s technical specification (ERD) so that the Planner, Worker, Judge, and operators can read and write campaign goals, agent configuration, task records, and video metadata in a consistent, queryable way. The schema MUST support the documented primary keys, foreign keys, and data types so that referential integrity is enforced and the system can join entities for reporting and audit.

**Why this priority**: The ERD is the source of truth for transactional and video metadata; without a schema that implements it, the system cannot persist state or replay tasks.

**Independent Test**: Create the schema (or apply migrations); insert one campaign, one agent linked to that campaign, one task linked to that campaign, and one video_asset linked to that agent and task; query by id and by relationship; verify foreign key constraints reject invalid references.

**Acceptance Scenarios**:

1. **Given** the schema is applied, **When** the system inserts a campaign with id, name, goal_description, status, created_at, updated_at, **Then** the row is stored and can be retrieved by id; the entity supports the attributes defined in the ERD.
2. **Given** the schema is applied, **When** the system inserts an agent with id, soul_md_path, character_reference_id, and campaign_id (referencing a campaign), **Then** the row is stored and the foreign key to campaigns is enforced; querying by campaign_id returns the agent(s) for that campaign.
3. **Given** the schema is applied, **When** the system inserts a task with id, campaign_id, task_type, priority, status, context (flexible structure, e.g. JSON), and created_at, **Then** the row is stored and the foreign key to campaigns is enforced.
4. **Given** the schema is applied, **When** the system inserts a video_asset with id, agent_id, task_id, platform, tier, character_reference_id, status, metadata (flexible structure), and created_at, **Then** the row is stored and foreign keys to agents and tasks are enforced; the entity supports the attributes defined in the ERD.

---

### User Story 2 - Relationships Match the ERD (Priority: P2)

As a developer or operator, I need the schema to implement the exact relationships defined in the project ERD: campaigns have zero or more agents and zero or more tasks; tasks produce zero or more video_assets; agents own zero or more video_assets. Foreign keys MUST be defined so that orphaned records are prevented and cascading or deletion rules are defined and consistent.

**Why this priority**: Correct relationships ensure that reporting (e.g. “all assets for this campaign”) and cleanup (e.g. “delete campaign and its tasks”) behave predictably.

**Independent Test**: Create entities in valid order (campaign → agent/task → video_asset); attempt to insert a video_asset with a non-existent agent_id or task_id and verify the insert is rejected; verify that querying a campaign returns its agents and tasks.

**Acceptance Scenarios**:

1. **Given** the schema, **When** a video_asset is inserted with agent_id or task_id that does not exist, **Then** the insert is rejected (referential integrity enforced).
2. **Given** the schema, **When** an agent is inserted with campaign_id that does not exist, **Then** the insert is rejected.
3. **Given** the schema, **When** a task is inserted with campaign_id that does not exist, **Then** the insert is rejected.
4. **Given** the schema, **When** an operator queries “all video_assets for campaign X” (via campaign → tasks → video_assets or campaign → agents → video_assets), **Then** the schema supports that query (e.g. via joins or indexed foreign keys).

---

### User Story 3 - Flexible Fields (Context, Metadata) Are Supported (Priority: P3)

As the system, I need the tasks and video_assets entities to support flexible, structured data (e.g. context and metadata) as defined in the ERD so that task context and asset metadata can be stored without schema changes for every new field. The schema MUST allow storing key-value or JSON-like structures for those columns.

**Why this priority**: Task context and video metadata vary by task type and platform; a fixed set of columns would be brittle.

**Independent Test**: Insert a task with context containing nested or varying keys; insert a video_asset with metadata containing duration, resolution, external_url; query and verify the flexible content is stored and retrievable.

**Acceptance Scenarios**:

1. **Given** the schema, **When** a task is stored with context containing goal_description, persona_constraints, required_resources (or equivalent structure per project contract), **Then** the full structure is persisted and can be read back without loss.
2. **Given** the schema, **When** a video_asset is stored with metadata containing optional fields (e.g. duration, resolution, external_url), **Then** the full structure is persisted and can be read back without loss.
3. **Given** the schema, **When** different tasks or assets have different keys in context or metadata, **Then** the schema accepts them (e.g. via a JSON or flexible column type) and does not require a fixed set of columns for every possible key.

---

### Edge Cases

- What happens when the schema is applied to an existing store that already has tables with the same names? The feature MUST support a defined migration or idempotent apply strategy (e.g. create-if-not-exists, or versioned migrations) so that deployments do not fail or lose data; the exact strategy is implementation-defined but MUST be documented.
- What happens when a campaign is deleted? The schema or application rules MUST define whether agents and tasks (and thus video_assets) are deleted, nullified, or retained; referential integrity (e.g. ON DELETE CASCADE or RESTRICT) MUST be explicit so that behaviour is predictable.
- What happens when timestamp or UUID types are not natively supported by the store? The schema definition MUST specify the logical types (UUID, timestamp) from the ERD; the implementation MAY map them to the nearest native type (e.g. string or binary for UUID) as long as the logical contract is preserved.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST provide a persistent schema (or migration set) that creates or updates the entities campaigns, agents, tasks, and video_assets with the attributes and types defined in the project technical specification (ERD in specs/technical.md).
- **FR-002**: The campaigns entity MUST have attributes: id (primary key), name, goal_description, status, created_at, updated_at; id MUST be a unique identifier (e.g. UUID).
- **FR-003**: The agents entity MUST have attributes: id (primary key), soul_md_path, character_reference_id, campaign_id (foreign key to campaigns); id MUST be a unique identifier.
- **FR-004**: The tasks entity MUST have attributes: id (primary key), campaign_id (foreign key to campaigns), task_type, priority, status, context (flexible or JSON-like), created_at; id MUST be a unique identifier.
- **FR-005**: The video_assets entity MUST have attributes: id (primary key), agent_id (foreign key to agents), task_id (foreign key to tasks), platform, tier, character_reference_id, status, metadata (flexible or JSON-like), created_at; id MUST be a unique identifier.
- **FR-006**: The schema MUST enforce referential integrity: agent.campaign_id → campaigns.id; task.campaign_id → campaigns.id; video_asset.agent_id → agents.id; video_asset.task_id → tasks.id. Inserts that violate these MUST be rejected.
- **FR-007**: The schema MUST support the relationships documented in the ERD: campaigns have zero or more agents and zero or more tasks; tasks produce zero or more video_assets; agents own zero or more video_assets.
- **FR-008**: The schema application (e.g. migration or init script) MUST be repeatable or idempotent so that deployments and tests can apply the schema without manual steps or data loss; the strategy MUST be documented.

### Key Entities

- **Campaign**: High-level objective or run; has id, name, goal_description, status, created_at, updated_at; has many agents and many tasks.
- **Agent**: Chimera agent configuration; has id, soul_md_path, character_reference_id, campaign_id (FK); belongs to one campaign; has many video_assets.
- **Task**: Persisted task record for audit/replay; has id, campaign_id (FK), task_type, priority, status, context (flexible), created_at; belongs to one campaign; may have many video_assets.
- **Video asset**: Metadata for a generated video (or image) asset; has id, agent_id (FK), task_id (FK), platform, tier, character_reference_id, status, metadata (flexible), created_at; belongs to one agent and one task.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: After applying the schema, the system can insert and retrieve campaigns, agents, tasks, and video_assets with all ERD-defined attributes; no required attribute is missing from the schema.
- **SC-002**: Referential integrity is enforced; inserting an agent, task, or video_asset with an invalid foreign key (non-existent parent) fails with a defined error.
- **SC-003**: Operators or the system can query “all tasks for campaign X” and “all video_assets for agent Y” (or equivalent) using the defined relationships; the schema supports these queries without full scans where the store supports indexing.
- **SC-004**: Task context and video_asset metadata can store flexible structures (e.g. JSON) as specified in the ERD; at least one round-trip store/read preserves the structure.

## Assumptions

- The authoritative definition of the ERD is in specs/technical.md (§4); any conflict between this spec and that document is resolved by the technical spec.
- The project has chosen a relational store (e.g. PostgreSQL) for this schema; the implementation will use that store’s native types (e.g. UUID, JSONB, timestamp) where they align with the ERD.
- Schema application is performed via migrations, init scripts, or a declarative tool; the exact mechanism is implementation-defined but MUST be repeatable and documented.
- Semantic memory (e.g. Weaviate) and queues (e.g. Redis) are out of scope; this feature covers only the relational schema for campaigns, agents, tasks, and video_assets.
