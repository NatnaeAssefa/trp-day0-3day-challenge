"""
Contract test: Task payload shape per specs/main/contracts/task-payload.json.
Validates that Task model and example payloads conform to the contract.
"""

import pytest
from pydantic import ValidationError

from src.models.task import Task, TaskContext


def test_task_payload_required_fields():
    """Task must have task_id, task_type, priority, context, created_at, status."""
    payload = {
        "task_id": "550e8400-e29b-41d4-a716-446655440000",
        "task_type": "generate_content",
        "priority": "high",
        "context": {"goal_description": "Create a post"},
        "created_at": "2026-02-04T12:00:00Z",
        "status": "pending",
    }
    t = Task.model_validate(payload)
    assert t.task_id == payload["task_id"]
    assert t.task_type == "generate_content"
    assert t.priority == "high"
    assert t.context.goal_description == "Create a post"
    assert t.status == "pending"


def test_task_payload_rejects_invalid_task_type():
    """task_type must be one of generate_content, reply_comment, execute_transaction."""
    payload = {
        "task_id": "550e8400-e29b-41d4-a716-446655440000",
        "task_type": "invalid_type",
        "priority": "high",
        "context": {"goal_description": "x"},
        "created_at": "2026-02-04T12:00:00Z",
        "status": "pending",
    }
    with pytest.raises(ValidationError):
        Task.model_validate(payload)


def test_task_payload_rejects_invalid_priority():
    """priority must be high, medium, or low."""
    payload = {
        "task_id": "550e8400-e29b-41d4-a716-446655440000",
        "task_type": "generate_content",
        "priority": "critical",
        "context": {"goal_description": "x"},
        "created_at": "2026-02-04T12:00:00Z",
        "status": "pending",
    }
    with pytest.raises(ValidationError):
        Task.model_validate(payload)


def test_task_payload_full_context():
    """context may include persona_constraints and required_resources."""
    payload = {
        "task_id": "550e8400-e29b-41d4-a716-446655440001",
        "task_type": "reply_comment",
        "priority": "medium",
        "context": {
            "goal_description": "Reply to comment",
            "persona_constraints": ["friendly", "brief"],
            "required_resources": ["mcp://twitter/mentions/123"],
        },
        "created_at": "2026-02-04T12:00:00Z",
        "status": "pending",
    }
    t = Task.model_validate(payload)
    assert t.context.persona_constraints == ["friendly", "brief"]
    assert t.context.required_resources == ["mcp://twitter/mentions/123"]
