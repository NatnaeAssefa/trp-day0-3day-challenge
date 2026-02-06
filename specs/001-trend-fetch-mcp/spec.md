# Feature Specification: Fetch Trends from MCP Resources

**Feature Branch**: `001-trend-fetch-mcp`  
**Created**: 2026-02-04  
**Status**: Draft  
**Input**: Fetch trends from MCP resources and return a list matching the Trend API contract (id, title, relevance_score, source, timestamp).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Planner Receives Trend Data for Planning (Priority: P1)

As a Planner (or any consumer of trend data), I need to request trend data from a configured resource and receive a list of trend items so that I can use them for content planning and task decomposition. Each item must include a unique id, title, relevance score, source, and timestamp so that I can filter, rank, and reason about trends without additional lookups.

**Why this priority**: Trend data is the primary input for the Planner’s perception layer; without it, the agent cannot react to current events or opportunities.

**Independent Test**: Call the trend-fetch capability with a valid resource identifier and optional time window; verify the response is a list and every item contains the five required fields with the correct types and value ranges.

**Acceptance Scenarios**:

1. **Given** a valid resource identifier, **When** the consumer requests trends, **Then** the system returns a list of items and each item has id (string), title (string), relevance_score (number between 0 and 1), source (string), and timestamp (string).
2. **Given** an optional time window, **When** the consumer requests trends with that window, **Then** the returned items are limited or filtered according to that window (e.g. only items within the window).
3. **Given** a resource that has no trends in the window, **When** the consumer requests trends, **Then** the system returns an empty list (not an error), and the consumer can proceed without failure.

---

### User Story 2 - Contract Compliance for Downstream Consumers (Priority: P2)

As a downstream consumer (e.g. tests, Planner logic, or another skill), I need the trend list to conform to the published Trend API contract so that I can rely on a stable shape and types without custom parsing or validation.

**Why this priority**: Contract stability enables independent testing and integration; without it, every consumer would need to handle multiple formats.

**Independent Test**: Request trends and assert that every item in the list satisfies the contract (required fields present, types correct, relevance_score in [0, 1]).

**Acceptance Scenarios**:

1. **Given** any successful trend response, **When** the consumer inspects each item, **Then** no item is missing id, title, relevance_score, source, or timestamp.
2. **Given** any trend item, **When** the consumer checks types, **Then** relevance_score is a number in the range 0.0 to 1.0 inclusive, and id, title, source, and timestamp are non-null strings.

---

### Edge Cases

- What happens when the resource is temporarily unavailable? The system SHOULD return an empty list or a defined error outcome so the consumer can decide whether to retry or skip; the exact behaviour is implementation-defined but MUST be consistent and documented for the consumer.
- What happens when the resource returns more items than the consumer needs? The system MAY support a limit or pagination; if not specified, a reasonable default (e.g. return up to a maximum number of items) applies so that responses remain bounded.
- What happens when the same trend appears from multiple sources? Each item MUST have a unique id; duplicates across sources MAY be represented as separate items with different source (and possibly different id) so that consumers can attribute by source.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST accept a resource identifier (e.g. URI or scheme) as input and return a list of trend items.
- **FR-002**: Each trend item in the returned list MUST include: id (string), title (string), relevance_score (number, 0.0–1.0), source (string), timestamp (string).
- **FR-003**: The system MUST support an optional time-window parameter so that trends can be scoped to a lookback period.
- **FR-004**: The system MUST obtain trend data from the external world only via the Model Context Protocol (MCP); no direct out-of-band API calls for this feature.
- **FR-005**: When no trends are available for the request, the system MUST return an empty list (or a defined, contract-compliant response) rather than failing the request with an ambiguous error.

### Key Entities

- **Trend item**: A single trend entry. Attributes: id (unique), title, relevance_score (0–1), source, timestamp. Represents one unit of trend data from a resource.
- **Resource (conceptual)**: A named or addressed source of trend data exposed via MCP (e.g. news, social). The feature consumes from it; it is not owned by this feature.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A consumer can request trends for a valid resource and receive a response within a reasonable time (e.g. under 30 seconds for a typical batch) so that the Planner can use trends in near-real-time planning.
- **SC-002**: One hundred percent of items in any successful trend response conform to the Trend API contract (all five fields present, correct types, relevance_score in range).
- **SC-003**: Contract tests (or equivalent) can validate the response shape and types without implementation knowledge; the feature is independently testable.
- **SC-004**: When the time-window parameter is supported, consumers can obtain trends limited to that window, improving relevance of results for planning.

## Assumptions

- The MCP layer and resource(s) are available and configured; this feature does not define how MCP servers are deployed or registered.
- The Trend API contract (id, title, relevance_score, source, timestamp) is the single source of truth for the output shape; it is defined in the project’s technical specification.
- Relevance scores are provided by the resource or computed in a way that yields a 0–1 value; no specific scoring algorithm is mandated by this spec.
- Timestamps are in a consistent format (e.g. ISO 8601) as defined by the technical contract.
