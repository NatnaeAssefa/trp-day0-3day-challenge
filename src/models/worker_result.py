"""
Worker result payload (Worker → Judge via ReviewQueue).
Conforms to specs/main/contracts/worker-result-payload.json and specs/technical.md §2.
"""

from datetime import datetime

from pydantic import BaseModel, Field


class WorkerResult(BaseModel):
    """Result pushed to ReviewQueue after a Worker completes a task."""

    task_id: str
    status: str = Field(..., pattern="^(success|failure)$")
    artifact: object | str | None = None
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    reasoning_trace: str | None = None
    created_at: datetime | str = Field(..., description="When the result was produced")
