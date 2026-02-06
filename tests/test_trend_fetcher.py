"""
Asserts that trend data structure matches the API contract in specs/technical.md §3.
Tests MUST fail until the trend fetcher returns the correct shape (TDD empty slot).
"""
import pytest

# Contract: each trend item MUST have id, title, relevance_score, source, timestamp
REQUIRED_TREND_FIELDS = ("id", "title", "relevance_score", "source", "timestamp")


def test_trend_fetcher_returns_list():
    """Trend fetcher must return a list (of trend items)."""
    from skills.skill_trend_fetcher import fetch_trends

    result = fetch_trends(resource_uri="news://test/trends")
    assert isinstance(result, list), "Trend API contract: output must be a list"


def test_trend_fetcher_items_have_required_fields():
    """Each trend item must have id, title, relevance_score, source, timestamp per specs/technical.md."""
    from skills.skill_trend_fetcher import fetch_trends

    result = fetch_trends(resource_uri="news://test/trends", time_range_hours=4)
    assert isinstance(result, list)
    for item in result:
        for field in REQUIRED_TREND_FIELDS:
            assert field in item, f"Trend item missing required field: {field}"
        assert isinstance(item["id"], str)
        assert isinstance(item["title"], str)
        assert isinstance(item["relevance_score"], (int, float))
        assert 0 <= item["relevance_score"] <= 1.0
        assert isinstance(item["source"], str)
        assert isinstance(item["timestamp"], str)
