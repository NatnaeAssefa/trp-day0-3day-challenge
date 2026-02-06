"""
Integration test: trend-fetch returns list conforming to Trend API; empty list when no trends.
Spec: specs/001-trend-fetch-mcp/spec.md.
"""

import pytest

from src.services.trend_fetcher import fetch_trends


def test_fetch_trends_returns_list():
    """Calling fetch_trends with a resource returns a list (possibly empty)."""
    result = fetch_trends("test://resource/trends")
    assert isinstance(result, list)


def test_fetch_trends_empty_resource_returns_empty_list():
    """When no trends available, return empty list per spec FR-005."""
    result = fetch_trends("test://empty/trends")
    assert result == []


def test_fetch_trends_each_item_has_required_fields():
    """When trends exist, each item has id, title, relevance_score, source, timestamp."""
    result = fetch_trends("test://resource/trends")
    for item in result:
        assert "id" in item
        assert "title" in item
        assert "relevance_score" in item
        assert "source" in item
        assert "timestamp" in item
        assert 0 <= item["relevance_score"] <= 1
