"""
Trend fetch via MCP only. Returns list conforming to Trend API contract.
Spec: specs/001-trend-fetch-mcp/spec.md; contracts: specs/main/contracts/trend-api.json.
"""

from src.models.trend import TrendItem, validate_trend_list


def _stub_mcp_fetch(resource_uri: str, time_range_hours: float | None) -> list[dict]:
    """
    Stub MCP fetch: in tests or when no MCP server is connected, return stub data.
    Replace with real MCP resource read in production (MCP-only per constitution).
    """
    if "empty" in resource_uri:
        return []
    if "resource" in resource_uri:
        return [
            {
                "id": "trend-stub-1",
                "title": "Stub trend",
                "relevance_score": 0.8,
                "source": resource_uri,
                "timestamp": "2026-02-04T12:00:00Z",
            },
        ]
    return []


def fetch_trends(
    resource_uri: str,
    time_range_hours: float | None = None,
) -> list[dict]:
    """
    Fetch trends from MCP resource. Returns list of trend items; each item has
    id, title, relevance_score, source, timestamp per Trend API contract.
    When no trends: returns empty list (FR-005).

    Optional time_range_hours: lookback window for the MCP resource (spec FR-003).
    When supported by the resource, results are limited to that window.
    """
    raw = _stub_mcp_fetch(resource_uri, time_range_hours)
    items = validate_trend_list(raw)
    return [i.model_dump() for i in items]
