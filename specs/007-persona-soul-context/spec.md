# Feature Specification: Load Agent Persona from SOUL.md and Inject into Context Assembly

**Feature Branch**: `007-persona-soul-context`  
**Created**: 2026-02-04  
**Status**: Draft  
**Input**: Load agent persona from SOUL.md and inject backstory, voice, and directives into LLM context assembly.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Agent Reasoning Uses Persona from SOUL.md (Priority: P1)

As the agent (or the system that runs the agent), I need the persona definition to be loaded from a designated file (SOUL.md) and included in the context that is assembled for each reasoning step so that the agent’s behaviour is consistent with its backstory, voice, and directives. The persona MUST be available before any reasoning or generation so that outputs align with the agent’s identity.

**Why this priority**: Persona is the "DNA" of the agent; without it in context, the agent cannot maintain consistent voice or respect directives.

**Independent Test**: Place a valid SOUL.md (or equivalent) with backstory, voice, and directives; trigger context assembly for a reasoning step; verify that the assembled context contains the backstory, voice, and directives from the file so that the reasoning step can use them.

**Acceptance Scenarios**:

1. **Given** a valid persona file (SOUL.md) at the designated path, **When** the system assembles context for an agent’s reasoning step, **Then** the assembled context includes the backstory, voice (or tone), and directives from that file in a form the reasoning step can use.
2. **Given** the persona file has been updated (e.g. new directives), **When** the system loads the persona for the next reasoning step, **Then** the loaded content reflects the current file (or a defined caching strategy) so that operators can change persona via the file without code changes.
3. **Given** multiple agents, **When** each agent’s context is assembled, **Then** each agent receives its own persona from its designated SOUL.md (or path) so that agents do not share or mix personas.

---

### User Story 2 - Backstory, Voice, and Directives Are Explicitly Injected (Priority: P2)

As an operator or auditor, I need the assembled context to clearly separate backstory, voice (or tone), and directives so that the reasoning step (and any downstream validation) can distinguish "who the agent is" from "how the agent speaks" and "what the agent must or must not do." The structure MUST be predictable so that prompts or templates can reference these sections.

**Why this priority**: Explicit structure supports consistency, testing, and the ability to override or extend (e.g. honesty directive) in a defined place.

**Independent Test**: Load a persona file that contains backstory, voice, and directives; assemble context; verify that the output has identifiable sections or fields for backstory, voice, and directives (or equivalent labels) so that a consumer can rely on their presence.

**Acceptance Scenarios**:

1. **Given** a persona file with backstory content, **When** context is assembled, **Then** the backstory is present in the context (e.g. in a "Backstory" or "Who you are" section or field) and is not mixed indistinguishably with other content.
2. **Given** a persona file with voice or tone guidelines, **When** context is assembled, **Then** the voice/tone is present (e.g. in a "Voice" or "Tone" section or field) so that the reasoning step can apply it to generation.
3. **Given** a persona file with directives (hard constraints or rules), **When** context is assembled, **Then** the directives are present (e.g. in a "Directives" or "Rules" section or field) so that the reasoning step can enforce them; directives are distinguishable from backstory and voice.

---

### User Story 3 - Context Assembly Is Repeatable and Traceable (Priority: P3)

As a developer or operator, I need the process that loads the persona and assembles the context to be repeatable (same inputs produce the same structure) and traceable so that I can debug or audit what persona was used for a given reasoning step. The source of the persona (e.g. file path or identifier) SHOULD be known so that version control or GitOps workflows can link behaviour to a specific file version.

**Why this priority**: Repeatability and traceability support testing and compliance (e.g. "which persona was active when this output was generated?").

**Independent Test**: Assemble context twice with the same persona file; verify the persona sections in the assembled context are identical. Verify that the system can report or log which persona source was used for a given assembly.

**Acceptance Scenarios**:

1. **Given** an unchanged persona file, **When** context is assembled twice, **Then** the persona content in the assembled context is the same both times (no non-deterministic injection).
2. **Given** a context assembly, **When** an operator or system needs to know the persona source, **Then** the source (e.g. path to SOUL.md or agent identifier) is available (e.g. in logs, metadata, or a defined API) so that behaviour can be traced to a file or version.
3. **Given** the persona file is missing or unreadable, **When** the system attempts to load it, **Then** the system does not proceed with an empty or undefined persona; it fails with a defined error or uses a safe default (e.g. minimal fallback) so that behaviour is predictable.

---

### Edge Cases

- What happens when the persona file is very large? The system MUST either support the full content in context (within the limits of the reasoning step’s context window) or apply a defined truncation or summarization strategy so that assembly always completes and the agent does not hang or omit persona arbitrarily.
- What happens when the file contains structured and unstructured parts (e.g. YAML frontmatter and markdown body)? The system MUST parse or separate these so that backstory, voice, and directives can be extracted and injected according to the project’s persona schema; the exact format (e.g. frontmatter + body) is defined elsewhere but the loader MUST handle it consistently.
- What happens when an agent has no SOUL.md or the path is not set? The system MUST not assume a default persona from another agent; it MUST fail clearly or use a documented "empty" or "minimal" persona so that behaviour is auditable.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST load the agent persona from a designated file (SOUL.md or a path configured per agent) before assembling the context for a reasoning step.
- **FR-002**: The loaded persona MUST include at least: backstory (narrative or biographical content), voice or tone (stylistic guidelines), and directives (hard constraints or rules). The system MUST inject all three into the assembled context.
- **FR-003**: The assembled context MUST make the persona content available to the reasoning step in a structured or clearly separated way (e.g. distinct sections or fields for backstory, voice, directives) so that the reasoning step can use them for generation and constraint enforcement.
- **FR-004**: Each agent MUST use its own persona source (one SOUL.md or path per agent); the system MUST NOT mix or reuse another agent’s persona for a given reasoning step unless explicitly configured as shared.
- **FR-005**: When the persona file is missing, unreadable, or invalid, the system MUST NOT proceed with an undefined or silent default; it MUST fail with a defined error or apply a documented minimal/fallback persona so that operators can detect misconfiguration.
- **FR-006**: The context assembly that includes the persona MUST be repeatable: for the same persona file content and same other inputs, the persona portion of the assembled context MUST be identical.
- **FR-007**: The system SHOULD support traceability of the persona source (e.g. file path, agent id) so that operators or auditors can determine which persona was used for a given reasoning step; the mechanism (log, metadata, or API) is implementation-defined.

### Key Entities

- **Persona**: The agent’s identity and behaviour definition, comprising backstory, voice (or tone), and directives. Loaded from SOUL.md (or equivalent).
- **SOUL.md (persona file)**: The designated file or document that stores the persona definition. Format and location are defined by the project (e.g. version-controlled, one per agent).
- **Assembled context**: The full context (persona + short-term history + long-term memories + other inputs) passed to the reasoning step. This feature ensures the persona portion is loaded from SOUL.md and injected.
- **Reasoning step**: The process that consumes the assembled context to produce agent output (e.g. reply, plan). Out of scope for this feature; this feature only ensures persona is in the context.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: When a valid SOUL.md is present, the assembled context for the agent’s reasoning step contains the backstory, voice, and directives from that file so that the agent can behave consistently.
- **SC-002**: Backstory, voice, and directives are identifiable as separate elements in the assembled context (e.g. by section or field name) so that tests or validators can assert their presence.
- **SC-003**: Loading the same persona file and assembling context twice yields the same persona content in the assembled context, so that behaviour is repeatable.
- **SC-004**: When the persona file is missing or invalid, the system does not silently proceed with an empty persona; a defined error or fallback behaviour occurs so that misconfiguration is visible.

## Assumptions

- The persona file format (e.g. SOUL.md with optional frontmatter and markdown body) is defined in the project’s technical or functional specification; this feature assumes that format and parses it to extract backstory, voice, and directives.
- "Context assembly" is the process that builds the full context (persona + other inputs) for the reasoning step; the reasoning step itself (e.g. model call) is out of scope.
- Persona may be cached in memory for performance, but the source of truth is the file; cache invalidation or refresh policy is implementation-defined.
- Multiple agents may each have their own SOUL.md path (e.g. per agent id or campaign); the system resolves the path per agent before loading.
