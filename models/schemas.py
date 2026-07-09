"""Pydantic models for request validation, internal data, and API responses."""

from typing import Literal

from pydantic import BaseModel, Field, field_validator
from config import config


class AgentRequest(BaseModel):
    """Request model for the /agent endpoint."""

    request: str

    @field_validator("request")
    @classmethod
    def validate_request(cls, v: str) -> str:
        """Reject empty or oversized requests."""
        stripped = v.strip()
        if not stripped:
            raise ValueError("Request must not be empty")
        if len(stripped) > config.MAX_REQUEST_LENGTH:
            raise ValueError(
                f"Request exceeds maximum length of {config.MAX_REQUEST_LENGTH} characters"
            )
        return stripped


class Task(BaseModel):
    """A single task within an execution plan."""

    id: int
    title: str
    description: str


class DocumentSection(BaseModel):
    """A generated section of the final document."""

    title: str
    content: str


class ReflectionResult(BaseModel):
    """Result of the reflection review cycle."""

    approved: bool
    missing: list[str] = Field(default_factory=list)
    issues: list[str] = Field(default_factory=list)


class AgentResponse(BaseModel):
    """Response model returned by the /agent endpoint."""

    status: Literal["completed", "error"]
    plan: list[str]
    document_path: str
