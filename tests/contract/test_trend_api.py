"""
Contract test: trend API response shape per specs/main/contracts/trend-api.json.
Each item must have id, title, relevance_score, source, timestamp.
"""

import pytest
from pydantic import ValidationError

from src.models.trend import TrendItem, validate_trend_list


def test_trend_item_required_fields():
    """Each trend item must have id, title, relevance_score, source, timestamp."""
    item = {
        "id": "trend-001",
        "title": "Summer fashion drop",
        "relevance_score": 0.85,
        "source": "news://ethiopia/fashion",
        "timestamp": "2026-02-04T12:00:00Z",
    }
    t = TrendItem.model_validate(item)
    assert t.id == "trend-001"
    assert t.title == "Summer fashion drop"
    assert t.relevance_score == 0.85
    assert t.source == "news://ethiopia/fashion"
    assert t.timestamp == "2026-02-04T12:00:00Z"


def test_trend_item_relevance_score_bounds():
    """relevance_score must be in [0.0, 1.0]."""
    valid = {
        "id": "x",
        "title": "x",
        "relevance_score": 0.0,
        "source": "x",
        "timestamp": "2026-02-04T12:00:00Z",
    }
    TrendItem.model_validate(valid)
    valid["relevance_score"] = 1.0
    TrendItem.model_validate(valid)
    invalid = {**valid, "relevance_score": 1.5}
    with pytest.raises(ValidationError):
        TrendItem.model_validate(invalid)
    invalid["relevance_score"] = -0.1
    with pytest.raises(ValidationError):
        TrendItem.model_validate(invalid)


def test_validate_trend_list_empty():
    """Empty list returns empty list of TrendItems."""
    assert validate_trend_list([]) == []


def test_validate_trend_list_multiple():
    """Multiple items all validated."""
    raw = [
        {
            "id": "a",
            "title": "A",
            "relevance_score": 0.5,
            "source": "s1",
            "timestamp": "2026-02-04T12:00:00Z",
        },
        {
            "id": "b",
            "title": "B",
            "relevance_score": 0.9,
            "source": "s2",
            "timestamp": "2026-02-04T13:00:00Z",
        },
    ]
    items = validate_trend_list(raw)
    assert len(items) == 2
    assert items[0].id == "a" and items[1].id == "b"
