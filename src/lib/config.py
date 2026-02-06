"""
Environment configuration. Redis URL, optional DB URL.
No hardcoded secrets; use env vars. See .env.example.
"""

import os


def get_redis_url() -> str:
    """Redis connection URL. Default: redis://localhost:6379/0."""
    return os.environ.get("REDIS_URL", "redis://localhost:6379/0")


def get_db_url() -> str | None:
    """PostgreSQL connection URL. None if not set (schema feature may be disabled)."""
    return os.environ.get("DATABASE_URL")
