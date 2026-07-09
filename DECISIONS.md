# DECISIONS.md

# Architecture Decision Records (ADR)

Version: 1.0

---

# Purpose

This document records the key architectural and engineering decisions made during the development of the Autonomous AI Engineer project.

Each decision includes:

* Context
* Decision
* Alternatives Considered
* Tradeoffs
* Rationale

This document serves as both project documentation and interview preparation material.

---

# ADR-001: FastAPI as the API Framework

## Context

The assignment requires exposing the autonomous agent through a REST API.

The API should be lightweight, easy to test, and production-oriented.

## Decision

Use **FastAPI**.

## Alternatives Considered

* Flask
* Django
* Flask + Flask-RESTX

## Rationale

FastAPI provides:

* Automatic request validation with Pydantic
* Automatic OpenAPI documentation
* Excellent performance
* Simple project structure
* Strong typing support

It is widely adopted for AI and machine learning services.

## Tradeoffs

Pros

* Modern
* Type-safe
* Easy to extend

Cons

* Slightly steeper learning curve than Flask

Decision Status

✅ Accepted

---

# ADR-002: Groq as the LLM Provider

## Context

The assignment requires a free or locally runnable language model.

## Decision

Use Groq with `llama-3.3-70b-versatile`.

## Alternatives Considered

* Gemini Free Tier
* Ollama
* LM Studio
* Grok

## Rationale

Groq offers:

* Fast inference
* Free developer access
* Reliable structured output
* Minimal setup

It enables rapid iteration during development and demo recording.

## Tradeoffs

Pros

* Very low latency
* High-quality responses
* Cloud-hosted

Cons

* Requires internet connectivity
* Depends on an external API

Decision Status

✅ Accepted

---

# ADR-003: Single-Agent Modular Architecture

## Context

The system could be implemented using either a single autonomous agent or multiple collaborating agents.

## Decision

Use a **single-agent architecture with modular components**.

Modules:

* Planner
* Executor
* Reflector
* DOCX Generator

## Alternatives Considered

* CrewAI
* LangGraph multi-agent workflow
* Planner/Writer/Reviewer agents

## Rationale

The assignment is constrained to 60 minutes.

A single-agent architecture reduces orchestration complexity while still demonstrating autonomous behavior.

Modular separation preserves extensibility.

## Tradeoffs

Pros

* Easier debugging
* Simpler implementation
* Lower token usage
* Easier interview explanation

Cons

* Less scalable for highly complex workflows

Decision Status

✅ Accepted

---

# ADR-004: Dynamic Planning

## Context

The agent could follow a predefined workflow or generate a plan dynamically.

## Decision

Generate an execution plan using the LLM.

## Alternatives Considered

* Hardcoded workflow
* Static task list

## Rationale

Dynamic planning demonstrates reasoning and autonomy.

Each request can generate a different execution plan depending on its complexity.

## Tradeoffs

Pros

* Flexible
* More intelligent
* Better demonstrates agentic behavior

Cons

* Requires validation of LLM output

Decision Status

✅ Accepted

---

# ADR-005: Sequential Task Execution

## Context

Tasks could be executed in parallel or sequentially.

## Decision

Execute tasks sequentially.

## Alternatives Considered

* Parallel execution
* Asynchronous execution

## Rationale

Sequential execution allows each task to use the outputs of previous tasks as context, resulting in a more coherent document.

It also keeps the implementation straightforward for the assignment.

## Tradeoffs

Pros

* Simpler logic
* Better document consistency
* Easier debugging

Cons

* Slower than parallel execution

Decision Status

✅ Accepted

---

# ADR-006: Reflection as the Mandatory Engineering Improvement

## Context

The assignment requires implementing one engineering improvement.

## Decision

Implement **Reflection / Self-Check**.

## Alternatives Considered

* Conversation memory
* Tool calling
* RAG
* Retry & fallback
* Guardrails

## Rationale

Reflection aligns naturally with document generation.

It demonstrates that the agent can evaluate and improve its own output before producing the final result.

This highlights reasoning and quality assurance without introducing unnecessary infrastructure.

## Tradeoffs

Pros

* Demonstrates autonomous quality control
* Improves document completeness
* Easy to explain in an interview

Cons

* Adds one additional LLM call

Decision Status

✅ Accepted

---

# ADR-007: JSON-Based Planning

## Context

The planner's output must be consumed programmatically.

## Decision

Require structured JSON output from the planner.

## Alternatives Considered

* Markdown
* Plain text
* Numbered lists

## Rationale

JSON is easy to validate using Pydantic and reduces parsing ambiguity.

## Tradeoffs

Pros

* Reliable parsing
* Strong validation
* Easier integration

Cons

* Requires prompt discipline

Decision Status

✅ Accepted

---

# ADR-008: python-docx for Document Generation

## Context

The final deliverable must be a Microsoft Word document.

## Decision

Use `python-docx`.

## Alternatives Considered

* Markdown export
* PDF generation
* HTML templates

## Rationale

`python-docx` is lightweight, well-supported, and generates native Word documents without requiring Microsoft Office.

## Tradeoffs

Pros

* Simple API
* Professional output
* Widely used

Cons

* Limited advanced formatting compared to Word

Decision Status

✅ Accepted

---

# ADR-009: Strict Separation of Responsibilities

## Context

Mixing planning, execution, API logic, and document generation leads to tightly coupled code.

## Decision

Assign one primary responsibility to each module.

* `planner.py` → Planning
* `executor.py` → Task execution
* `reflector.py` → Quality review
* `doc_generator.py` → Document creation
* `llm.py` → LLM communication

## Rationale

This improves readability, testing, and maintainability while making the code easier to explain.

## Tradeoffs

Pros

* High cohesion
* Low coupling
* Easier testing

Cons

* Slightly more files

Decision Status

✅ Accepted

---

# ADR-010: Scope Control

## Context

Many additional features could be added, but the assignment is time-limited.

## Decision

Limit the MVP to the assignment requirements.

Explicitly exclude:

* Databases
* Authentication
* Frontend
* Docker
* Multi-agent orchestration
* RAG
* Persistent memory
* Streaming responses

## Rationale

Focusing on the required functionality improves code quality and ensures the solution remains achievable within the allotted time.

## Tradeoffs

Pros

* Faster implementation
* Cleaner architecture
* Better focus

Cons

* Fewer production features

Decision Status

✅ Accepted

---

# Summary

The architecture emphasizes:

* Simplicity over unnecessary complexity
* Modularity over monolithic design
* Explainability over novelty
* Reliability over feature count

These decisions align with the assignment's evaluation criteria and provide a strong foundation for future enhancements without compromising the MVP.
