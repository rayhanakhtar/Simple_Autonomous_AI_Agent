"""Planner module for converting requests into structured execution plans."""

import json
import logging

from pydantic import ValidationError

from agent.llm import LLMClient
from agent.prompts import PLANNER_SYSTEM_PROMPT, PLANNER_USER_TEMPLATE
from models.schemas import Task

logger = logging.getLogger(__name__)


class Planner:
    """Converts a natural language request into an ordered list of tasks."""

    def __init__(self, llm_client: LLMClient) -> None:
        self._llm = llm_client

    def create_plan(self, request: str) -> list[Task]:
        """Generate and validate an execution plan for the given request."""
        user_prompt = PLANNER_USER_TEMPLATE.format(request=request)
        raw = self._llm.generate(PLANNER_SYSTEM_PROMPT, user_prompt)
        tasks = self._parse_and_validate(raw)

        if tasks is not None:
            logger.info("Plan created with %d tasks", len(tasks))
            return tasks

        logger.warning("First plan attempt failed validation, retrying...")
        raw = self._llm.generate(PLANNER_SYSTEM_PROMPT, user_prompt)
        tasks = self._parse_and_validate(raw)

        if tasks is not None:
            logger.info("Plan created on retry with %d tasks", len(tasks))
            return tasks

        logger.error("Planner failed to produce valid JSON after retry")
        raise RuntimeError("Planner could not generate a valid execution plan")

    @staticmethod
    def _clean_json_output(raw: str) -> str:
        """Extract JSON object from LLM output, stripping fences or text."""
        start = raw.find("{")
        end = raw.rfind("}")
        if start != -1 and end != -1 and end > start:
            return raw[start:end + 1].strip()
        return raw.strip()

    def _parse_and_validate(self, raw: str) -> list[Task] | None:
        """Parse JSON from LLM output and validate against Task schema."""
        cleaned = self._clean_json_output(raw)
        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError as e:
            logger.error("Invalid JSON from planner: %s", e)
            return None

        tasks_raw = data.get("tasks", [])
        if not tasks_raw:
            logger.error("No tasks found in planner output")
            return None

        try:
            return [Task.model_validate(t) for t in tasks_raw]
        except ValidationError as e:
            logger.error("Task validation failed: %s", e)
            return None
