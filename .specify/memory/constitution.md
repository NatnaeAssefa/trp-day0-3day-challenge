<!--
  Sync Impact Report
  Version change: (template/placeholder) → 1.0.0
  Modified principles: N/A (initial fill)
  Added sections: N/A
  Removed sections: N/A
  Templates: plan-template.md ✅ updated (Constitution Check); spec-template.md ✅ no change; tasks-template.md ✅ updated (Notes: TDD + Traceability)
  .specify/templates/commands/*.md: N/A (path not present)
  Follow-up TODOs: None
-->

# Project Chimera Constitution

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)

Implementation MUST NOT be written until the relevant behaviour is specified and ratified in the `specs/` directory. Code and tests MUST reference spec documents and contracts by name. If a feature is not described in `specs/_meta.md`, `specs/functional.md`, `specs/technical.md`, or an optional spec (e.g. `specs/openclaw_integration.md`), it is out of scope until the spec is updated first.

**Rationale:** Ambiguity leads to agent hallucination and scope creep. The SRS and specs are the single source of truth; implementation is executable intent derived from them.

### II. MCP-Only External I/O

All perception (Resources), action (Tools), and prompts for external systems MUST go through the Model Context Protocol (MCP). Direct API calls from agent core logic are prohibited. Platform volatility (e.g. social API changes) is absorbed at the MCP Server layer.

**Rationale:** Decouples agent reasoning from integration details; enables swapping data sources and tools without changing Planner/Worker/Judge logic; aligns with SRS §3.2.

### III. Test-First (TDD)

Tests MUST be written to assert contracts (e.g. API shape, skill I/O) before implementation. Tests SHOULD fail initially to define the "empty slots" that implementation fills. Red–Green–Refactor applies: failing test → implement → passing test → refactor.

**Rationale:** Ensures code aligns with specs and prevents drift; enables safe refactoring and agent-driven implementation against clear goals.

### IV. Judge as Gatekeeper

Only the Judge may commit Worker results to GlobalState. Human-in-the-Loop (HITL) is implemented at the Judge layer only. Confidence thresholds and sensitive-topic overrides are defined in the functional spec and enforced at the Judge. No human approval inside Planner or Worker execution paths.

**Rationale:** Single enforcement point for quality and safety; clear audit trail; SRS §5.1 and NFR 1.x require HITL at the Judge.

### V. Traceability & Compliance

Before writing code, the implementer MUST state the plan and name the spec(s) being implemented. Tests MUST assert against contracts in `specs/technical.md` and skill I/O in `skills/*/README.md`. All PRs and reviews MUST verify spec alignment and absence of hardcoded secrets (per security policy).

**Rationale:** Ensures every change is traceable to ratified intent and reduces unspecified behaviour or security gaps.

## Additional Constraints

- **Source of truth:** The Project Chimera SRS (in `docs/`) is the authoritative system specification. The `specs/` directory is the executable intent; any conflict is resolved by the SRS.
- **Skills vs MCP:** Skills (in `skills/`) are runtime capability packages with I/O contracts in READMEs; MCP Servers are external bridges. Do not confuse skill interfaces with MCP tool definitions. Document developer MCPs in `research/tooling_strategy.md`.
- **Technology:** Python 3.11+; dependencies and tooling defined in `pyproject.toml`. Tests run via `make test` or `pytest`; Docker and CI must pass tests per `.github/workflows/main.yml`.

## Development Workflow

- **Before coding:** Check `specs/` for the feature; name the spec and plan in 1–2 sentences.
- **Before merge:** Run `make test` (or equivalent); run `make spec-check` where available. AI review (e.g. CodeRabbit) MUST check spec alignment and security (no hardcoded secrets).
- **Commit discipline:** Commit early and often; history should tell a story of evolving complexity. Minimum 2 commits per day during active development (per challenge guidelines).

## Governance

- This constitution supersedes ad-hoc practices for Project Chimera. All work MUST comply with the Core Principles.
- **Amendments:** Require documentation of the change, rationale, and (if breaking) a migration or transition plan. Update this file and the version/date footer; increment version per semantic rules below.
- **Versioning:** MAJOR = backward-incompatible principle removal or redefinition; MINOR = new principle or materially expanded guidance; PATCH = clarifications, typos, non-semantic refinements.
- **Compliance review:** PRs and reviews MUST verify alignment with Spec-Driven Development, MCP-Only I/O, TDD, Judge as Gatekeeper, and Traceability. Use `.cursor/rules/chimera.mdc` for agent runtime guidance.

**Version**: 1.0.0 | **Ratified**: 2026-02-04 | **Last Amended**: 2026-02-04
