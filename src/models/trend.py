"""
Trend API: list of trend items (MCP response shape).
Conforms to specs/main/contracts/trend-api.json and specs/technical.md §3.
"""

from pydantic import BaseModel, Field


class TrendItem(BaseModel):
    """Single trend entry. Required: id, title, relevance_score, source, timestamp."""

    id: str
    title: str
    relevance_score: float = Field(..., ge=0.0, le=1.0)
    source: str
    timestamp: str  # ISO 8601 or Unix ms


def validate_trend_list(items: list[dict]) -> list[TrendItem]:
    """Validate and return a list of TrendItem from raw MCP response."""
    return [TrendItem.model_validate(i) for i in items]
