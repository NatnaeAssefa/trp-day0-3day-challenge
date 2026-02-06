# Specs Meta — Project Chimera

## Vision

**Project Chimera** is an **autonomous influencer factory**: a system that builds and operates digital entities (Chimera Agents) that research trends, generate content, and manage engagement with minimal human intervention.

- **Internal coordination:** Hierarchical **Planner–Worker–Judge** swarm (FastRender pattern). The Planner decomposes goals into tasks; Workers execute single tasks via MCP Tools; the Judge validates outputs and commits to GlobalState or escalates to HITL.
- **External interaction:** All external I/O (social APIs, news, memory, commerce) is performed **only** through the **Model Context Protocol (MCP)**. No direct API calls from agent core logic.
- **Governance:** Human-in-the-Loop is enforced at the **Judge** layer via confidence scoring and sensitive-topic filters. The Judge is the single gatekeeper for committing Worker results.

## Constraints

1. **Spec-driven development:** Implementation MUST NOT be written until the relevant behaviour is specified and ratified in this `specs/` directory. Code and tests MUST reference spec documents and contracts by name.
2. **No implementation without ratified spec:** If a feature is not described in `_meta.md`, `functional.md`, or `technical.md` (or an optional spec such as `openclaw_integration.md`), it is out of scope unless the spec is updated first.
3. **MCP for all external I/O:** Perception (Resources), action (Tools), and prompts are exclusively via MCP. Platform volatility is absorbed at the MCP Server layer.
4. **HITL and Judge as gatekeeper:** Only the Judge may commit Worker results to GlobalState. Confidence thresholds and sensitive-topic overrides are defined in the functional spec and implemented at the Judge.

## Spec Index

| Spec | Purpose |
|------|---------|
| [_meta.md](_meta.md) | Vision, constraints, and spec index (this file). |
| [functional.md](functional.md) | User stories and functional requirements; traceability to SRS FRs. |
| [technical.md](technical.md) | API contracts (JSON), database ERD (video metadata and related entities), MCP tool references. |
| [openclaw_integration.md](openclaw_integration.md) | Optional: how Chimera publishes availability/status to an OpenClaw-style agent network. |

## Source of Truth

The [Project Chimera SRS](../docs/Project%20Chimera%20SRS%20Document_%20Autonomous%20Influencer%20Network.md) is the authoritative system specification. This `specs/` directory is the **executable intent** derived from the SRS for implementation and agent guidance. Any conflict is resolved by the SRS.
