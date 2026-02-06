# Data Model — Project Chimera Core

**Branch**: `main`  
**Phase**: 1 (Design)  
**Source**: [specs/technical.md](../technical.md) §4; [spec.md](spec.md).

This document summarises entities, fields, relationships, validation rules, and state transitions for the Chimera core implementation scope (features 001–008).

---

## 1. Entity summary

| Entity | Purpose | Storage |
|--------|---------|---------|
| **Campaign** | Top-level goal container; has agents and tasks | PostgreSQL `campaigns` |
| **Agent** | Chimera identity; SOUL path, character reference; belongs to campaign | PostgreSQL `agents` |
| **Task** | Unit of work (Planner → Worker); persisted for audit | PostgreSQL `tasks` + Redis TaskQueue |
| **VideoAsset** | Generated video/image metadata; produced by task, owned by agent | PostgreSQL `video_assets` |
| **TrendItem** | Single trend entry (id, title, relevance_score, source, timestamp) | In-memory / MCP response; not persisted in this schema |
| **WorkerResult** | Worker output with confidence_score; consumed by Judge | Redis ReviewQueue; committed state in GlobalState / DB |

---

## 2. PostgreSQL entities

### 2.1 campaigns

| Field | Type | Description |
|-------|------|-------------|
| id | UUID PK | Primary key. |
| name | string | Campaign name. |
| goal_description | string | High-level goal for the campaign. |
| status | string | Campaign lifecycle status. |
| created_at | timestamp | Creation time. |
| updated_at | timestamp | Last update. |

**Relationships:** One campaign has zero or more agents; one campaign has zero or more tasks.

### 2.2 agents

| Field | Type | Description |
|-------|------|-------------|
| id | UUID PK | Primary key. |
| soul_md_path | string | Path to SOUL.md (persona). |
| character_reference_id | string | Consistency lock for visual/content (SRS FR 3.1). |
| campaign_id | UUID FK → campaigns | Owning campaign. |

**Relationships:** Many agents belong to one campaign; one agent has zero or more video_assets.

### 2.3 tasks

| Field | Type | Description |
|-------|------|-------------|
| id | UUID PK | Primary key (matches task_id in queue payload). |
| campaign_id | UUID FK → campaigns | Campaign this task belongs to. |
| task_type | string | `generate_content` \| `reply_comment` \| `execute_transaction`. |
| priority | string | `high` \| `medium` \| `low`. |
| status | string | `pending` \| `in_progress` \| `review` \| `complete`. |
| context | JSONB | goal_description, persona_constraints, required_resources (MCP URIs). |
| created_at | timestamp | Creation time. |

**Relationships:** Many tasks belong to one campaign; one task may produce zero or more video_assets. **Validation:** task_type and priority must match allowed enums; context must include required fields per [technical.md](../technical.md) §1.

### 2.4 video_assets

| Field | Type | Description |
|-------|------|-------------|
| id | UUID PK | Primary key. |
| agent_id | UUID FK → agents | Owning agent. |
| task_id | UUID FK → tasks | Task that produced this asset. |
| platform | string | Target platform (e.g. instagram, tiktok). |
| tier | string | `tier1` \| `tier2`. |
| character_reference_id | string | Consistency lock. |
| status | string | `draft` \| `judge_pending` \| `approved` \| `published` \| `rejected`. |
| metadata | JSONB | duration, resolution, external_url, etc. |
| created_at | timestamp | Creation time. |

**Relationships:** Many video_assets belong to one agent and one task. **State transitions:** draft → judge_pending → approved/rejected; approved → published.

---

## 3. Queue payloads (in-memory / Redis)

- **Task (Planner → TaskQueue):** task_id (UUID), task_type, priority, context (goal_description, persona_constraints, required_resources), assigned_worker_id, created_at, status. See [contracts/task-payload.json](contracts/task-payload.json) and [technical.md](../technical.md) §1.
- **Worker Result (Worker → ReviewQueue):** task_id, status (success \| failure), artifact, confidence_score (0.0–1.0), reasoning_trace, created_at. See [contracts/worker-result-payload.json](contracts/worker-result-payload.json) and [technical.md](../technical.md) §2.

---

## 4. Trend API (MCP response shape)

- **TrendItem:** id (string), title (string), relevance_score (0.0–1.0), source (string), timestamp (string). See [contracts/trend-api.json](contracts/trend-api.json) and [technical.md](../technical.md) §3.

---

## 5. Validation rules (from requirements)

- **Task:** task_type ∈ { generate_content, reply_comment, execute_transaction }; priority ∈ { high, medium, low }; status ∈ { pending, in_progress, review, complete }. context.required_resources must be valid MCP resource URIs where applicable.
- **Worker Result:** confidence_score ∈ [0.0, 1.0]; status ∈ { success, failure }; task_id must match an existing Task.
- **Trend item:** relevance_score ∈ [0.0, 1.0]; id, title, source, timestamp non-null strings.
- **video_assets.status:** Values as above; transitions enforced at Judge/HITL layer.

All implementation and tests MUST conform to these entities and contracts.
