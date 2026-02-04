# Chimera Agent Skills

**Skills** are reusable capability packages that the Chimera agent (Workers) call at runtime. They are distinct from **MCP Servers**: skills are the internal interface the agent uses; they may call MCP Tools or external APIs under the hood.

## Skill Model

- Each skill lives in its own directory: `skills/skill_<name>/`.
- Each skill **MUST** have a `README.md` that defines:
  - **Input contract:** Parameters (names, types, required/optional). These are what the Planner/Worker must pass.
  - **Output contract:** Shape of the return value (e.g. list of trend items, transcript text). Must align with [specs/technical.md](../specs/technical.md) where applicable.
- Implementation can be a stub initially; the **structure and contracts** must be ready so that:
  - Tests can assert that skill modules accept the correct parameters (see `tests/test_skills_interface.py`).
  - Future implementation can fill in the logic without changing the contract.

## Naming

- Directory: `skill_<capability>` (e.g. `skill_trend_fetcher`, `skill_transcribe_audio`).
- Callable: Can be a function or class method; the README defines the effective signature.

## Index

| Skill | Input (summary) | Output (summary) | Spec reference |
|-------|-----------------|------------------|----------------|
| [skill_trend_fetcher](skill_trend_fetcher/README.md) | resource_uri, optional time_range_hours | List of trend items (id, title, relevance_score, source, timestamp) | technical.md §3 Trend API |
| [skill_download_youtube](skill_download_youtube/README.md) | video_url, format (e.g. audio/video) | local_path or blob reference | — |
| [skill_transcribe_audio](skill_transcribe_audio/README.md) | audio_url or audio_path | transcript (string) | — |

All output shapes that represent “trends” MUST conform to the Trend API contract in `specs/technical.md`.
