# Project Chimera — Autonomous Influencer Network

Spec-driven, Planner–Worker–Judge (FastRender) autonomous influencer system. All external I/O via **Model Context Protocol (MCP)**.

## Structure

- **specs/** — Source of truth for behaviour: _meta, functional, technical, openclaw_integration.
- **research/** — Architecture strategy, tooling strategy.
- **skills/** — Agent runtime skills (contracts in READMEs; stubs for TDD).
- **tests/** — Failing tests defining the “empty slots” (run with `make test` or `pytest`).

## Setup

- **Python:** 3.11+. Recommended: `uv` (`uv sync` then `uv run pytest tests/`).
- **Tenx MCP Sense:** Keep connected in the IDE for challenge telemetry. Confirm connection with the same GitHub account used for submission.

## Commands

- `make setup` — Install dependencies (`uv sync` or `pip install -e .`).
- `make test` — Run tests (Docker build + run, or `pytest` locally).
- `make spec-check` — Verify specs/_meta.md, functional.md, technical.md.
- `make lint` — Run ruff check and format check (requires `pip install ruff`).

**Quickstart:** See [specs/main/quickstart.md](specs/main/quickstart.md) for setup, test commands, and implementation order (features 001–008).

## Specs

Implement only what is in **specs/**. See `.cursor/rules/chimera.mdc` for the Prime Directive and traceability.

## AI review

`.coderabbit.yaml` configures the AI reviewer to check **Spec Alignment** (code traceable to specs/) and **Security** (no hardcoded secrets). If CodeRabbit is not used, apply the same checks via PR checklist or another review tool.
