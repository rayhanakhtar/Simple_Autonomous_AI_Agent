"""FastAPI application entry point for the Autonomous AI Engineer."""

import logging
from fastapi import FastAPI
from config import config

logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Autonomous AI Engineer",
    description="An autonomous AI agent that plans, executes, and generates professional documents.",
    version="1.0.0",
)


@app.get("/")
def health_check():
    """Return API health status."""
    logger.info("Health check requested")
    return {"status": "healthy", "service": "Autonomous AI Engineer"}
