"""LLM client for communicating with Groq API."""

import logging
import time
from groq import (
    Groq,
    APIError,
    APIConnectionError,
    APITimeoutError,
    RateLimitError,
    InternalServerError,
)
from config import config

logger = logging.getLogger(__name__)

_TRANSIENT_ERRORS = (APIConnectionError, APITimeoutError, RateLimitError, InternalServerError)


class LLMClient:
    """Client for interacting with the Groq language model."""

    def __init__(self) -> None:
        config.validate()
        self._client = Groq(api_key=config.GROQ_API_KEY)
        self._model = config.MODEL_NAME
        self._max_retries = config.MAX_RETRIES

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """Send prompts to the LLM and return the generated text."""
        last_error: Exception | None = None

        for attempt in range(self._max_retries + 1):
            try:
                response = self._client.chat.completions.create(
                    model=self._model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                )
                content = response.choices[0].message.content or ""
                logger.info("LLM response received (%d chars)", len(content))
                return content.strip()

            except _TRANSIENT_ERRORS as e:
                last_error = e
                if attempt < self._max_retries:
                    delay = 0.5 * (2 ** attempt)
                    logger.warning(
                        "Transient LLM error (attempt %d/%d): %s. Retrying in %.1fs...",
                        attempt + 1,
                        self._max_retries + 1,
                        e,
                        delay,
                    )
                    time.sleep(delay)

            except APIError as e:
                logger.error("Non-retryable API error: %s", e)
                raise

        logger.error("LLM failed after %d attempts", self._max_retries + 1)
        raise RuntimeError(f"LLM request failed after {self._max_retries + 1} attempts") from last_error
