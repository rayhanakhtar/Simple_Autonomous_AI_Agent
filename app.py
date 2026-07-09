"""FastAPI application entry point for the Autonomous AI Engineer."""

import logging
import traceback

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from config import config
from agent.llm import LLMClient
from agent.planner import Planner
from agent.executor import Executor
from agent.reflector import Reflector
from tools.doc_generator import create_document
from models.schemas import AgentRequest, AgentResponse

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

llm_client = LLMClient()
planner = Planner(llm_client)
executor = Executor(llm_client)
reflector = Reflector(llm_client, executor)


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Convert Pydantic validation errors to HTTP 400."""
    logger.warning("Validation error: %s", exc.errors())
    return JSONResponse(
        status_code=400,
        content={"detail": exc.errors()[0]["msg"] if exc.errors() else "Invalid request"},
    )


@app.get("/")
def health_check() -> dict:
    """Return API health status."""
    return {"status": "healthy", "service": "Autonomous AI Engineer"}


@app.post("/agent")
def process_request(body: AgentRequest) -> AgentResponse:
    """Handle a natural language request and return a generated document."""
    request_text = body.request
    logger.info("Request received: %.80s", request_text)
    try:
        logger.info("Planner started")
        plan = planner.create_plan(request_text)
        plan_titles = [t.title for t in plan]
        logger.info("Planner completed: %d tasks", len(plan_titles))
        logger.info("Executor started")
        sections = executor.execute(plan, request_text)
        logger.info("Executor completed: %d sections", len(sections))
        logger.info("Reflection started")
        sections = reflector.review(sections, request_text, plan_titles)
        logger.info("Reflection completed: %d sections", len(sections))
        logger.info("Document generation started")
        doc_path = create_document(sections)
        logger.info("Document generated: %s", doc_path)
        logger.info("Response returned")
        return AgentResponse(status="completed", plan=plan_titles, document_path=doc_path)
    except HTTPException:
        raise
    except ValueError as e:
        logger.error("Request validation error: %s", e)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        logger.error("Unexpected error: %s", traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail="An internal error occurred while processing your request.",
        )
