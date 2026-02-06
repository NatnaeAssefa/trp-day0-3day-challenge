"""
Trend fetcher skill. Contract: specs/technical.md §3 Trend API.
Returns list of items with id, title, relevance_score, source, timestamp.
Data obtained via MCP only (see src.services.trend_fetcher).
"""


def fetch_trends(resource_uri: str, time_range_hours: float | None = None) -> list[dict]:
    """Fetch trends from MCP resource. Delegates to src.services.trend_fetcher."""
    from src.services.trend_fetcher import fetch_trends as _fetch

    return _fetch(resource_uri=resource_uri, time_range_hours=time_range_hours)
