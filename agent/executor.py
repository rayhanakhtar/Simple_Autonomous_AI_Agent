"""Executor module for processing planned tasks into document sections."""

import json
import logging

from pydantic import ValidationError

from agent.llm import LLMClient
from agent.prompts import EXECUTOR_SYSTEM_PROMPT, EXECUTOR_USER_TEMPLATE
from models.schemas import Task, DocumentSection

logger = logging.getLogger(__name__)


class Executor:
    """Executes each planned task sequentially and collects document sections."""

    def __init__(self, llm_client: LLMClient) -> None:
        self._llm = llm_client

    def execute(self, plan: list[Task], request: str) -> list[DocumentSection]:
        """Execute each task in order and return generated sections."""
        sections: list[DocumentSection] = []

        for task in plan:
            logger.info("Executing task %d: %s", task.id, task.title)
            section = self._execute_task(task, request, sections)
            if section is not None:
                sections.append(section)
                logger.info("Task %d completed: %s", task.id, task.title)
            else:
                logger.warning("Task %d produced no output: %s", task.id, task.title)

        logger.info("Executor finished: %d sections generated", len(sections))
        return sections

    def _execute_task(
        self,
        task: Task,
        request: str,
        previous_sections: list[DocumentSection],
    ) -> DocumentSection | None:
        """Generate a single document section for the given task."""
        previous_text = self._format_previous_sections(previous_sections)
        current_task_text = f"Task Title: {task.title}\nTask Description: {task.description}"

        user_prompt = EXECUTOR_USER_TEMPLATE.format(
            request=request,
            previous_sections=previous_text,
            current_task=current_task_text,
        )

        raw = self._llm.generate(EXECUTOR_SYSTEM_PROMPT, user_prompt)
        return self._parse_section(raw, task.title)

    @staticmethod
    def _format_previous_sections(sections: list[DocumentSection]) -> str:
        """Format completed sections into a readable context string."""
        if not sections:
            return "None yet."
        parts = [f"{s.title}\n{s.content}" for s in sections]
        return "\n\n---\n\n".join(parts)

    @staticmethod
    def _parse_section(raw: str, expected_title: str) -> DocumentSection | None:
        """Parse and validate a single section from LLM output."""
        start = raw.find("{")
        end = raw.rfind("}")
        if start == -1 or end == -1 or end <= start:
            logger.error("No JSON object found in executor output")
            return None

        cleaned = raw[start:end + 1]
        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError as e:
            logger.error("Invalid JSON from executor: %s", e)
            return None

        try:
            section = DocumentSection.model_validate(data)
        except ValidationError as e:
            logger.error("Section validation failed: %s", e)
            return None

        if section.title != expected_title:
            logger.warning(
                "Title mismatch: expected '%s', got '%s'. Using expected title.",
                expected_title, section.title,
            )
            section.title = expected_title

        return section
