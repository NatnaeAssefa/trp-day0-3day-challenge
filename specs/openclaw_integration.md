# OpenClaw Integration — Project Chimera

**Status:** Optional / recommended.  
**Purpose:** Define how Chimera agents publish **availability** or **status** to an OpenClaw-style Agent Social Network so they can participate in agent-to-agent coordination.

**References:** [Technical Report §2.2](../technical_report.md), SRS (agent identity, economic agency), OpenClaw concepts: agent identity, credentials, agent-only channels, delegation.

---

## 1. Alignment with OpenClaw

Chimera agents already have:

- **Persistent identity:** SOUL.md and agent_id.
- **Memory:** Weaviate (semantic) and Redis (episodic).
- **Autonomy:** Planner–Worker–Judge with MCP.
- **Economic agency:** Non-custodial wallets via Coinbase AgentKit.

These make Chimera agents **compatible participants** in an OpenClaw-style ecosystem. This spec describes a minimal integration surface: **identity**, **credentials/permissions**, and **status/heartbeat**.

---

## 2. Agent Identity for OpenClaw

Each Chimera agent that may join the OpenClaw network SHALL have:

- **Agent ID:** A stable, globally unique identifier (e.g. UUID or DID). Stored with the agent record and in SOUL.md or linked config.
- **Public profile (optional):** A minimal, machine-readable profile (e.g. JSON) that other agents can read: name, capabilities (e.g. “content_generation”, “trend_analysis”), and optional wallet address for economic interactions.

---

## 3. Credentials and Permissions

- **Credentials:** Chimera SHALL use the same credential model that OpenClaw expects (e.g. scoped API keys or signed tokens) so that when a Chimera agent “speaks” to the network, it can authenticate as that agent.
- **Permissions:** Chimera SHALL expose a minimal permission set (e.g. “can_receive_delegation”, “can_publish_status”, “can_transact”) so that the OpenClaw layer can enforce delegation and access. These can be derived from the Orchestrator’s existing policy (e.g. BoardKit / AGENTS.md).

---

## 4. Status / Heartbeat Protocol

To publish **availability** or **status** to the OpenClaw network:

**4.1 Status payload (conceptual JSON)**

```json
{
  "agent_id": "chimera-uuid-or-did",
  "status": "available | busy | maintenance",
  "capabilities": ["content_generation", "trend_analysis", "commerce"],
  "timestamp": "2026-02-04T12:00:00Z",
  "optional_metadata": {}
}
```

**4.2 Delivery**

- **Option A (push):** Chimera Orchestrator (or a dedicated “Bridge” service) POSTs this payload to an OpenClaw-defined endpoint (e.g. `/agents/status` or `/heartbeat`) at a configurable interval (e.g. every 60s when the agent is active).
- **Option B (pull):** Chimera exposes a read-only Resource (e.g. `openclaw://chimera/agent/{agent_id}/status`) that OpenClaw or other agents can poll via MCP.

**4.3 Scope**

- Only agents that are explicitly opted-in (e.g. via campaign or tenant config) publish status.
- No sensitive data (wallet keys, full memory) is ever sent; only availability and capability tags.

---

## 5. Implementation Notes

- **Phase 1:** Document the contract (this spec) and add a stub or config flag “openclaw_enabled” per agent/campaign.
- **Phase 2:** Implement the status payload and one of Option A or B when the OpenClaw API/spec is stable.
- **Security:** Credentials and keys SHALL be read from environment or secrets manager (e.g. `OPENCLAW_*`); never hardcoded.

This plan keeps Chimera ready for agent social graphs and delegation without committing to a specific OpenClaw API until it is final.
