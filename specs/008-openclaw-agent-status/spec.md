# Feature Specification: Publish Chimera Agent Availability/Status to OpenClaw-Style Network for Discovery

**Feature Branch**: `008-openclaw-agent-status`  
**Created**: 2026-02-04  
**Status**: Draft  
**Input**: Publish Chimera agent availability/status to an OpenClaw-style network for agent-to-agent discovery.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Chimera Agents Are Discoverable by Other Agents (Priority: P1)

As another agent or an orchestrator on an OpenClaw-style network, I need to discover which Chimera agents are available and what they can do so that I can delegate work, coordinate, or transact with them. The system MUST publish each opted-in Chimera agent’s availability (or status) and a minimal set of capabilities to the network at a defined interval or on demand, so that discovery is possible without exposing sensitive data.

**Why this priority**: Discovery is the entry point for agent-to-agent coordination; without published status, Chimera agents are invisible to the network.

**Independent Test**: Opt in one Chimera agent; trigger status publish (or wait for interval); verify that the network (or a test endpoint) receives a status payload that includes the agent identifier, availability/status, and capability tags, and that no secrets or full memory are included.

**Acceptance Scenarios**:

1. **Given** a Chimera agent that is opted in to the OpenClaw-style network, **When** the system publishes status, **Then** the network receives a payload that includes at least: a stable agent identifier, a status value (e.g. available, busy, maintenance), and a list of capability tags (e.g. content_generation, trend_analysis) so that other agents can find and reason about this agent.
2. **Given** the status payload is published, **When** another agent or discovery service queries the network, **Then** they can find this Chimera agent by identifier or by capability and see its current availability so that they can decide whether to contact or delegate to it.
3. **Given** a Chimera agent that is not opted in, **When** the system runs, **Then** that agent’s status is not published to the network so that only explicitly participating agents are visible.

---

### User Story 2 - Status Payload Is Bounded and Safe (Priority: P2)

As a security or compliance stakeholder, I need the published status to contain only non-sensitive, discovery-oriented data (agent id, status, capabilities, timestamp) and never secrets, keys, or full memory so that participation in the network does not create new exposure.

**Why this priority**: Publishing to an external network increases attack surface; the payload MUST be minimal and safe.

**Independent Test**: Publish status for an agent that has credentials, wallet, and memory; verify that the payload contains only the allowed fields and that no credential, key, or memory content appears in the published data.

**Acceptance Scenarios**:

1. **Given** any Chimera agent, **When** status is published to the OpenClaw-style network, **Then** the payload includes only: agent identifier, status (availability), capabilities (list of tags), timestamp, and optional metadata that is explicitly allowed (e.g. public profile summary); it MUST NOT include wallet private keys, API keys, or full memory content.
2. **Given** the status payload, **When** an auditor inspects it, **Then** they can confirm that the payload conforms to the defined schema (e.g. agent_id, status, capabilities, timestamp) and that no sensitive fields are present.
3. **Given** credentials or keys are required to authenticate the publish request to the network, **When** the system sends the request, **Then** those credentials are obtained from a secure source (e.g. environment or secrets manager) and are never embedded in the status payload or in logs.

---

### User Story 3 - Opt-In and Configurable Publish (Priority: P3)

As an operator, I need to control which Chimera agents publish to the OpenClaw-style network and at what interval (or trigger) so that we can roll out participation gradually and avoid publishing when agents are in a maintenance or test environment. The publish behaviour MUST be configurable per agent or per campaign/tenant.

**Why this priority**: Opt-in and configuration prevent accidental exposure and allow safe experimentation.

**Independent Test**: Set an agent to opted-out (or disable the feature); verify no status is published for that agent. Set an agent to opted-in; verify status is published according to the configured interval or trigger.

**Acceptance Scenarios**:

1. **Given** an agent or tenant configuration that disables OpenClaw-style publishing, **When** the system runs, **Then** no status is published for that agent (or those agents) so that they do not appear on the network.
2. **Given** an agent or tenant configuration that enables publishing, **When** the configured interval elapses (or the trigger fires), **Then** the system publishes the current status for that agent so that the network sees up-to-date availability.
3. **Given** a configurable publish interval (e.g. every 60 seconds when active), **When** the operator sets the interval, **Then** the system respects it so that network load and freshness are controllable.

---

### Edge Cases

- What happens when the OpenClaw-style network or endpoint is temporarily unavailable? The system MUST NOT retry indefinitely without bound; it MAY retry with backoff and MUST NOT block the rest of the Chimera system; failed publishes MAY be logged or surfaced so that operators can fix connectivity.
- What happens when the agent has no stable identifier yet? The system MUST NOT publish until the agent has a valid identifier (e.g. from agent record or SOUL.md); publishing without an identifier would make discovery or attribution impossible.
- What happens when multiple Chimera agents are opted in? Each agent’s status is published with its own agent_id so that the network can distinguish them; no single payload should represent multiple agents unless the network protocol explicitly supports that.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST support publishing each opted-in Chimera agent’s availability or status to an OpenClaw-style network (or designated discovery endpoint) so that other agents can discover Chimera agents for coordination or delegation.
- **FR-002**: The published status payload MUST include at least: a stable agent identifier, a status value (e.g. available, busy, maintenance), a list of capability tags (e.g. content_generation, trend_analysis, commerce), and a timestamp so that discovery and freshness are supported.
- **FR-003**: The status payload MUST NOT contain sensitive data: no wallet private keys, no API keys, no full memory or persona content; only non-sensitive, discovery-oriented fields are allowed. Credentials used to authenticate the publish request MUST be obtained from a secure source (e.g. environment or secrets manager), not from the payload or code.
- **FR-004**: Only Chimera agents that are explicitly opted in (e.g. via agent config, campaign config, or tenant config) SHALL have their status published; opted-out or unconfigured agents MUST NOT be published.
- **FR-005**: The system MUST support a configurable publish interval or trigger (e.g. when agent is active, every N seconds) so that operators can control how often status is sent and avoid unbounded traffic.
- **FR-006**: When the network or endpoint is unavailable, the system MUST NOT block the rest of the Chimera system; it MAY retry with backoff and SHOULD log or surface failures so that operators can act.
- **FR-007**: Each published payload MUST be associated with a single agent (one agent_id per payload) so that the network can attribute status to the correct Chimera agent; the agent MUST have a stable identifier before any publish.

### Key Entities

- **OpenClaw-style network**: The external agent social network or discovery layer to which Chimera publishes status. Protocol and endpoint are defined by the network; this feature produces the payload and sends it (or exposes it for pull).
- **Status payload**: The data published for one agent: agent_id, status, capabilities, timestamp, and optional allowed metadata. Conforms to a defined schema so that the network and other agents can parse it.
- **Opted-in agent**: A Chimera agent that is configured to participate in the OpenClaw-style network; only these agents have their status published.
- **Capability tags**: A list of machine-readable tags (e.g. content_generation, trend_analysis, commerce) that describe what the agent can do; used by other agents for discovery and delegation decisions.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Other agents or discovery services can find opted-in Chimera agents on the OpenClaw-style network (or via the designated mechanism) and see their current availability and capabilities so that agent-to-agent discovery is possible.
- **SC-002**: One hundred percent of published status payloads contain only the allowed, non-sensitive fields; no audit finds credentials, keys, or full memory in the payload.
- **SC-003**: Opted-out agents do not appear on the network; when an agent is disabled for publishing, no status is sent for that agent so that participation is controllable.
- **SC-004**: Status is published at the configured interval or on the configured trigger so that the network has up-to-date availability without unbounded publish traffic.

## Assumptions

- The OpenClaw-style network (or equivalent) defines or will define the exact endpoint, protocol, and payload schema; this feature aligns with the project’s openclaw_integration spec and implements the minimal surface (identity, status, capabilities) so that Chimera can integrate when the network API is stable.
- Chimera agents have a stable identifier (e.g. UUID or DID) from the agent record or SOUL.md; this feature does not create the identifier but requires it to be present before publishing.
- Credentials for authenticating to the network (e.g. API keys, signed tokens) are provided by the operator via environment or secrets manager; this feature consumes them but does not define how they are issued.
- "OpenClaw-style" means a network that supports agent identity, status, and discovery; the implementation may target a specific OpenClaw API or a compatible stub for testing until the API is final.
