# Functional Specification — Project Chimera

User stories and functional requirements, with traceability to the SRS. All behaviour must be implementable from these stories and the contracts in [technical.md](technical.md).

---

## Perception & Trend Fetching

**SRS ref:** FR 2.0, FR 2.1, FR 2.2

- **As a Planner,** I need to receive filtered updates from configured MCP Resources (e.g. `news://ethiopia/fashion/trends`, `twitter://mentions/recent`) so that I only react to relevant signals.
- **As the system,** I need to pass ingested content through a Semantic Filter that scores relevance against the agent’s active goals, and only create tasks when the score exceeds the configured Relevance Threshold (e.g. 0.75).
- **As a Planner,** I need Trend Alerts from a background Trend Spotter (aggregated over a time window) so that I can create content-creation tasks when a cluster of related topics emerges.

---

## Content Generation (Creative Engine)

**SRS ref:** FR 3.0, FR 3.1, FR 3.2

- **As a Worker,** I need to generate text (captions, scripts, replies) via the Cognitive Core and images/video via MCP Tools (e.g. ideogram, runway, luma) so that content is produced in a platform-consistent way.
- **As a Worker,** I need every image generation request to include the agent’s `character_reference_id` (or style LoRA) so that the virtual influencer remains visually consistent.
- **As a Planner,** I need to choose between Tier 1 (image-to-video, daily content) and Tier 2 (text-to-video, hero content) based on task priority and budget so that we balance quality and cost.

---

## Action System (Social Interface)

**SRS ref:** FR 4.0, FR 4.1

- **As a Worker,** I need to perform all social actions (post, reply, like) only via MCP Tools (e.g. `twitter.post_tweet`, `instagram.publish_media`) so that governance, rate limiting, and dry-run are enforced in one layer.
- **As the system,** I need a full loop: Ingest (Planner receives comment via Resource) → Plan (reply task) → Generate (Worker consults Memory, generates reply) → Act (Worker calls tool) → Verify (Judge confirms before tool execution finalises).

---

## Human-in-the-Loop (HITL)

**SRS ref:** NFR 1.0, NFR 1.1, NFR 1.2

- **As the Judge,** I need to attach a `confidence_score` (0.0–1.0) to every Worker output so that routing is deterministic.
- **As the Judge,** I need to route results as follows: High (>0.90) → auto-approve; Medium (0.70–0.90) → async approval (dashboard queue); Low (<0.70) → reject and signal Planner to retry.
- **As the Judge,** I need to send any content that triggers sensitive-topic filters (Politics, Health Advice, Financial Advice, Legal Claims) to the HITL queue regardless of confidence.

---

## Agentic Commerce & Budget

**SRS ref:** FR 5.0, FR 5.1, FR 5.2

- **As an agent,** I need a non-custodial wallet (Coinbase AgentKit) per Chimera identity so that I can transact on-chain without per-action human approval.
- **As a Worker,** I need to propose transactions via MCP/AgentKit; the CFO Judge must approve or reject based on budget limits and anomaly detection.
- **As the Planner,** I need to check balance (e.g. `get_balance`) before starting cost-incurring workflows.

---

## Orchestration & Swarm

**SRS ref:** FR 6.0, FR 6.1

- **As the system,** I need a Planner Service that reads GlobalState (campaign goals), generates tasks, and pushes them to TaskQueue (Redis).
- **As the system,** I need a Worker Pool that pops tasks from TaskQueue, executes them with MCP Tools, and pushes results to ReviewQueue.
- **As the system,** I need a Judge Service that pops from ReviewQueue, validates output (including OCC), and either commits to GlobalState or re-queues for the Planner.
- **As the Judge,** I need to implement Optimistic Concurrency Control: if GlobalState has changed since the Worker started the task, I invalidate the result and re-queue for re-planning.

---

## Persona & Memory

**SRS ref:** FR 1.0, FR 1.1, FR 1.2

- **As an agent,** I need my persona defined in SOUL.md (backstory, voice, directives) and hydrated at runtime so that behaviour is consistent and version-controlled.
- **As the system,** I need hierarchical memory retrieval: short-term (Redis episodic) and long-term (Weaviate semantic) assembled into context before each reasoning step.
- **As the Judge,** I need to trigger updates to long-term memory (Weaviate) when high-engagement interactions are approved, so that the persona can evolve within guardrails.

---

## Traceability Summary

| SRS section | Covered in |
|-------------|------------|
| FR 1.x Cognitive Core & Persona | Persona & Memory |
| FR 2.x Perception | Perception & Trend Fetching |
| FR 3.x Creative Engine | Content Generation |
| FR 4.x Action System | Action System |
| FR 5.x Agentic Commerce | Agentic Commerce & Budget |
| FR 6.x Orchestration | Orchestration & Swarm |
| NFR 1.x HITL | Human-in-the-Loop |
