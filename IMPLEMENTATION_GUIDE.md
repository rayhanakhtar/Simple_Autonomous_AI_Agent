# IMPLEMENTATION_GUIDE.md

# Autonomous AI Engineer – Implementation Guide

Version: 1.0

---

# Purpose

This document provides the implementation blueprint for the Autonomous AI Engineer project.

It complements `AGENT.md` by specifying:

* implementation order
* file responsibilities
* expected classes
* expected functions
* data flow
* coding conventions
* error handling
* testing expectations

Follow this document during implementation.

---

# Development Principles

The implementation must follow these principles:

* One file = One responsibility
* One class = One responsibility
* One function = One job
* Prefer composition over large monolithic classes
* Keep the code readable and interview-friendly
* Avoid premature optimization
* Write code that can be explained in under five minutes

---

# Implementation Order

Implement the project in the following sequence.

## Phase 1

Project setup

Create project structure.

Install dependencies.

Configure environment variables.

---

## Phase 2

Data models

Create Pydantic request and response models.

Define internal task and document section models.

---

## Phase 3

LLM client

Implement the Groq client.

This should be completed before any planner or executor logic.

---

## Phase 4

Planner

Implement task planning.

Return validated JSON.

---

## Phase 5

Executor

Execute planner tasks sequentially.

Store generated sections.

---

## Phase 6

Reflection

Review generated sections.

Generate missing content if required.

---

## Phase 7

DOCX generation

Generate the final Microsoft Word document.

---

## Phase 8

FastAPI integration

Expose the `/agent` endpoint.

Wire all modules together.

---

## Phase 9

Testing

Run both required assignment scenarios.

---

# File Responsibilities

## app.py

Purpose:

FastAPI application entry point.

Responsibilities:

* initialize FastAPI
* register routes
* validate requests
* orchestrate modules
* return responses

Must not contain:

* planning logic
* execution logic
* prompt engineering

---

## config.py

Responsibilities:

* load environment variables
* expose configuration values
* validate API keys
* centralize constants

Expected values:

* GROQ_API_KEY
* MODEL_NAME
* OUTPUT_DIRECTORY
* MAX_RETRIES
* LOG_LEVEL

---

## models/schemas.py

Create all Pydantic models.

Suggested models:

AgentRequest

```python
request: str
```

Task

```python
id: int
title: str
description: str
```

DocumentSection

```python
title: str
content: str
```

ReflectionResult

```python
approved: bool
missing: list[str]
```

AgentResponse

```python
status: str
plan: list[str]
document_path: str
```

---

## agent/llm.py

Purpose

Centralized LLM wrapper.

Create one class:

LLMClient

Public methods:

```python
generate(system_prompt, user_prompt)
```

Responsibilities:

* communicate with Groq
* retry transient failures
* return clean text

Never place business logic here.

---

## agent/prompts.py

Purpose

Store prompt templates.

Separate prompts into constants or helper functions.

Required prompts:

Planner Prompt

Executor Prompt

Reflection Prompt

No API calls should occur in this file.

---

## agent/planner.py

Create one class:

Planner

Public method:

```python
create_plan(request)
```

Input:

Natural language request.

Output:

Validated list of Task objects.

Responsibilities:

* call planner prompt
* validate JSON
* return structured tasks

Planner must never generate report content.

---

## agent/executor.py

Create one class:

Executor

Public method:

```python
execute(plan, request)
```

Responsibilities:

Loop over tasks.

Generate one section at a time.

Store completed sections.

Return ordered list of DocumentSection objects.

---

## agent/reflector.py

Create one class:

Reflector

Public method:

```python
review(sections)
```

Responsibilities:

Evaluate generated sections.

Return ReflectionResult.

Generate missing sections when necessary.

Maximum two review cycles.

---

## tools/doc_generator.py

Purpose

Generate Microsoft Word documents.

Public function:

```python
create_document(sections)
```

Responsibilities:

* create document
* apply headings
* save file
* return path

No LLM calls.

---

# Data Flow

The implementation should follow this sequence.

```text
Request
    │
    ▼
Planner
    │
    ▼
Task List
    │
    ▼
Executor
    │
    ▼
Sections
    │
    ▼
Reflection
    │
    ▼
Approved Sections
    │
    ▼
DOCX Generator
    │
    ▼
Response
```

No shortcuts should bypass this workflow.

---

# Logging Strategy

Every major stage should emit logs.

Suggested events:

INFO

Request received

INFO

Planner started

INFO

Planner finished

INFO

Executing task

INFO

Reflection completed

INFO

Document saved

INFO

Response returned

ERROR

LLM failure

ERROR

Document generation failure

---

# Error Handling Strategy

Validation errors

Return HTTP 400.

Planner failures

Retry once.

Reflection failures

Skip additional review.

Document generation failure

Return HTTP 500.

Unexpected exceptions

Return generic error.

Never expose stack traces.

---

# Function Design Guidelines

Functions should:

* perform one task
* return predictable values
* avoid side effects
* include type hints
* include docstrings

Prefer small helper functions over long methods.

---

# Naming Conventions

Classes

PascalCase

Functions

snake_case

Variables

snake_case

Constants

UPPER_CASE

Private helpers

_prefix_name

---

# Dependency Rules

Allowed:

Planner → LLM

Executor → LLM

Reflector → LLM

Document Generator → python-docx

App → all modules

Not allowed:

Planner → DOCX

Executor → FastAPI

Reflector → FastAPI

LLM → Planner

Avoid circular imports.

---

# Testing Checklist

The implementation is complete only if the following pass.

## Test Case 1

Input

Create meeting minutes for a product roadmap discussion.

Expected

* planner creates tasks
* executor generates sections
* reflection approves
* DOCX generated

---

## Test Case 2

Input

Create a proposal for an AI recruitment assistant.

Budget under $20,000.

Timeline three months.

Use assumptions where information is missing.

Expected

* planner creates dynamic task list
* assumptions generated
* timeline included
* budget included
* risks included
* reflection identifies missing sections if necessary
* DOCX generated

---

# Code Quality Checklist

Before finalizing, verify:

✓ Modular architecture

✓ Type hints

✓ Pydantic validation

✓ Structured logging

✓ Retry logic

✓ Reflection implemented

✓ No duplicated code

✓ No business logic in app.py

✓ Clean folder organization

✓ Interview-ready code

---

# Future Enhancements (Out of Scope)

The following are intentionally excluded from the MVP but should be considered for future versions:

* Conversation memory
* Retrieval-Augmented Generation (RAG)
* Multi-agent architecture
* Tool calling with external APIs
* Persistent storage (SQLite/PostgreSQL)
* Asynchronous task execution
* Streaming responses
* User authentication
* Background job queue (Celery/RQ)
* PDF export
* Web UI

These features are omitted to keep the implementation focused, modular, and achievable within the assignment's 60-minute constraint.
