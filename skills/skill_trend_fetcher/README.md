# Skill: Trend Fetcher

Fetches trend data from a configured MCP Resource (e.g. news, social) and returns a list of trend items that conform to the **Trend API contract** in [specs/technical.md](../../specs/technical.md).

## Input Contract

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `resource_uri` | str | Yes | MCP resource URI (e.g. `news://ethiopia/fashion/trends`, `twitter://trending`). |
| `time_range_hours` | float | No | Lookback window in hours. Default behaviour (if omitted): implementation-defined (e.g. 24). |

**Example call:**

```python
fetch_trends(resource_uri="news://ethiopia/fashion/trends", time_range_hours=4)
```

## Output Contract

Returns a **list** of trend items. Each item MUST have at least:

| Field | Type | Description |
|-------|------|-------------|
| `id` | str | Unique identifier for the trend item. |
| `title` | str | Short title or headline. |
| `relevance_score` | float | 0.0–1.0. |
| `source` | str | Source identifier or URI. |
| `timestamp` | str | ISO 8601 or Unix ms. |

**Example:**

```json
[
  {
    "id": "trend-001",
    "title": "Summer fashion drop",
    "relevance_score": 0.85,
    "source": "news://ethiopia/fashion",
    "timestamp": "2026-02-04T12:00:00Z"
  }
]
```

Tests in `tests/test_trend_fetcher.py` assert that the fetcher’s return value matches this structure.

## Implementation Status

Stub/structure only. Implementation will use MCP Resources and optional semantic filtering per SRS FR 2.0–2.2.
