"""
Redis queue adapter for TaskQueue and ReviewQueue.
Push/pop with env-based connection (REDIS_URL).
"""

import json
from typing import Any

from src.lib.config import get_redis_url

# Queue key names per specs (Planner → TaskQueue, Worker → ReviewQueue)
TASK_QUEUE_KEY = "chimera:task_queue"
REVIEW_QUEUE_KEY = "chimera:review_queue"


def _client():
    """Lazy Redis client to avoid import-time connection."""
    import redis

    url = get_redis_url()
    return redis.from_url(url, decode_responses=True)


def push_task_queue(payload: dict[str, Any]) -> None:
    """Push a Task payload to the task queue."""
    c = _client()
    c.rpush(TASK_QUEUE_KEY, json.dumps(payload, default=str))


def pop_task_queue() -> dict[str, Any] | None:
    """Pop a Task payload from the task queue. Returns None if empty."""
    c = _client()
    raw = c.lpop(TASK_QUEUE_KEY)
    if raw is None:
        return None
    return json.loads(raw)


def push_review_queue(payload: dict[str, Any]) -> None:
    """Push a WorkerResult payload to the review queue."""
    c = _client()
    c.rpush(REVIEW_QUEUE_KEY, json.dumps(payload, default=str))


def pop_review_queue() -> dict[str, Any] | None:
    """Pop a WorkerResult payload from the review queue. Returns None if empty."""
    c = _client()
    raw = c.lpop(REVIEW_QUEUE_KEY)
    if raw is None:
        return None
    return json.loads(raw)
