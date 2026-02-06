# Contracts — Project Chimera Core

**Branch**: `main`  
**Source**: [specs/technical.md](../../technical.md).

This directory holds machine-readable contracts for the Chimera core. All implementation and tests MUST conform to these shapes.

| File | Description |
|------|-------------|
| [task-payload.json](task-payload.json) | Agent Task (Planner → Worker via TaskQueue). SRS §6.2 Schema 1. |
| [worker-result-payload.json](worker-result-payload.json) | Worker Result (Worker → Judge via ReviewQueue). |
| [trend-api.json](trend-api.json) | Trend API: list of trend items (id, title, relevance_score, source, timestamp). |

Canonical narrative definitions remain in [specs/technical.md](../../technical.md). These JSON Schema files are for validation and code generation.
