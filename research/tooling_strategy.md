# Tooling Strategy — Project Chimera

Separation of **developer tools (MCP)** and **agent skills (runtime)** per the Challenge. This document lists MCP servers used during development and how they are configured. Runtime skills are defined under `skills/`.

---

## 1. Developer Tools (MCP)

These MCP servers support the **developer** in the IDE or CLI, not the Chimera agent at runtime.

| MCP Server | Purpose | Configuration |
|------------|---------|---------------|
| **Tenx MCP Sense** | Telemetry and “Black Box” flight recorder for the challenge. Tracks thinking and interaction for assessment. | Connected via Cursor IDE MCP settings. Must remain connected; use same GitHub account as submission. |
| **Filesystem / Cursor built-in** | File read/write, search, edit during development. | IDE default. |
| **Git (if used)** | Version control operations from the agent (e.g. status, diff). Optional. | Configure in `.cursor/mcp.json` or IDE MCP if added. |

**Note:** No production secrets or API keys in MCP config; use environment variables and `.env` (gitignored) for runtime and external services.

---

## 2. Runtime vs Developer

| Category | Where | Used by |
|----------|--------|---------|
| **Developer MCPs** | This document; Cursor MCP config | Human developer / IDE agent during coding. |
| **Agent skills (runtime)** | `skills/` directory; each skill has a README with I/O contract | Chimera Workers at runtime (invoked as capability packages; may call MCP tools under the hood). |
| **MCP Servers for agents** | Deployed alongside Orchestrator (e.g. mcp-server-twitter, mcp-server-weaviate) | Agent runtime (MCP Host); not necessarily the same as developer MCPs. |

The Chimera agent **never** uses Tenx MCP Sense or dev-only filesystem MCPs for its perception/action loop; those are for development and assessment only.

---

## 3. Adding New Developer MCPs

When adding an MCP server for development:

1. Add it to the table in §1 with purpose and configuration.
2. Ensure it does not expose production credentials; use env vars where needed.
3. Keep `research/tooling_strategy.md` updated so the team (and assessors) know the tooling split.
