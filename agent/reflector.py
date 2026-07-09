"""Reflector module for reviewing generated content and filling gaps."""

import json
import logging

from pydantic import ValidationError

from agent.llm import LLMClient
from agent.executor import Executor
from agent.prompts import REFLECTOR_SYSTEM_PROMPT, REFLECTOR_USER_TEMPLATE
from models.schemas import Task, DocumentSection, ReflectionResult

logger = logging.getLogger(__name__)

MAX_REVIEW_CYCLES = 2


class Reflector:
    """Reviews generated sections and triggers regeneration of missing content."""

    def __init__(self, llm_client: LLMClient, executor: Executor) -> None:
        self._llm = llm_client
        self._executor = executor

    def review(
        self,
        sections: list[DocumentSection],
        request: str,
        plan_titles: list[str],
    ) -> list[DocumentSection]:
        """Evaluate sections and fill missing content. Max 2 cycles."""
        current_sections = list(sections)

        for cycle in range(MAX_REVIEW_CYCLES):
            logger.info("Reflection cycle %d/%d", cycle + 1, MAX_REVIEW_CYCLES)
            result = self._run_review(current_sections, request, plan_titles)

            if result is None:
                logger.warning("Reflection could not parse result, stopping review")
                break

            if result.approved:
                logger.info("Reflection approved (%d sections)", len(current_sections))
                return current_sections

            if not result.missing:
                logger.info("Reflection not approved but no missing sections listed")
                break

            logger.info("Missing sections detected: %s", result.missing)
            generated = self._generate_missing(result.missing, request, current_sections)
            current_sections.extend(generated)

            if cycle == MAX_REVIEW_CYCLES - 1:
                logger.info("Max review cycles reached, returning best available")

        return current_sections

    def _run_review(
        self,
        sections: list[DocumentSection],
        request: str,
        plan_titles: list[str],
    ) -> ReflectionResult | None:
        """Execute one reflection review and parse the result."""
        sections_summary = self._format_sections_summary(sections)
        plan_list = "\n".join(f"- {t}" for t in plan_titles)

        user_prompt = REFLECTOR_USER_TEMPLATE.format(
            request=request,
            plan_titles=plan_list,
            sections_summary=sections_summary,
        )

        raw = self._llm.generate(REFLECTOR_SYSTEM_PROMPT, user_prompt)
        return self._parse_result(raw)

    @staticmethod
    def _format_sections_summary(sections: list[DocumentSection]) -> str:
        """Format section titles and content previews for the reflector prompt."""
        if not sections:
            return "No sections generated yet."
        parts = []
        for s in sections:
            preview = s.content[:200].replace("\n", " ")
            if len(s.content) > 200:
                preview += "..."
            parts.append(f"- {s.title}: {preview}")
        return "\n\n".join(parts)

    @staticmethod
    def _parse_result(raw: str) -> ReflectionResult | None:
        """Parse and validate the reflection result from LLM output."""
        start = raw.find("{")
        end = raw.rfind("}")
        if start == -1 or end == -1 or end <= start:
            logger.error("No JSON object found in reflection output")
            return None

        try:
            data = json.loads(raw[start:end + 1])
        except json.JSONDecodeError as e:
            logger.error("Invalid JSON from reflector: %s", e)
            return None

        try:
            return ReflectionResult.model_validate(data)
        except ValidationError as e:
            logger.error("Reflection result validation failed: %s", e)
            return None

    def _generate_missing(
        self,
        missing_titles: list[str],
        request: str,
        existing: list[DocumentSection],
    ) -> list[DocumentSection]:
        """Generate content for missing sections using the executor."""
        tasks = [
            Task(id=i + 1, title=title, description=f"Generate {title} section.")
            for i, title in enumerate(missing_titles)
        ]

        logger.info("Generating %d missing sections", len(tasks))

        plan = self._executor.execute(tasks, request)
        existing_titles = {s.title for s in existing}

        new_sections = [s for s in plan if s.title not in existing_titles]
        if new_sections:
            logger.info("Generated %d new sections", len(new_sections))
        else:
            logger.warning("No new sections could be generated")

        return new_sections
