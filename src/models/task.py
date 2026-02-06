"""
Task payload (Planner → Worker via TaskQueue).
Conforms to specs/main/contracts/task-payload.json and specs/technical.md §1.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class TaskContext(BaseModel):
    """Context for a task: goal, persona constraints, required MCP resources."""

    goal_description: str
    persona_constraints: list[str] = Field(default_factory=list)
    required_resources: list[str] = Field(default_factory=list)


class Task(BaseModel):
    """Agent task payload. Required: task_id, task_type, priority, context, created_at, status."""

    task_id: str  # UUID v4 string
    task_type: str = Field(
        ...,
        pattern="^(generate_content|reply_comment|execute_transaction)$",
    )
    priority: str = Field(..., pattern="^(high|medium|low)$")
    context: TaskContext
    assigned_worker_id: str | None = None
    created_at: datetime | str = Field(..., description="ISO 8601 or Unix ms")
    status: str = Field(
        ...,
        pattern="^(pending|in_progress|review|complete)$",
    )
