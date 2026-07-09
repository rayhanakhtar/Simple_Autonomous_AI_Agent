# AGENT.md

# Autonomous AI Engineer – System Specification

Version: 1.0

---

# Purpose

This document is the master engineering specification for the Autonomous AI Engineer assignment.

It defines the system architecture, implementation requirements, coding standards, project philosophy, engineering constraints, and acceptance criteria.

This document serves as the primary reference for implementation. All project files, modules, prompts, APIs, and documentation must follow the specifications defined here.

The implementation should prioritize software engineering quality, maintainability, modularity, and explainability over unnecessary complexity.

---

# Project Objective

Build an autonomous AI agent capable of:

1. Understanding a natural language business request.
2. Planning its own execution steps.
3. Executing those steps autonomously.
4. Evaluating the generated work.
5. Producing a polished Microsoft Word (.docx) document.
6. Returning both the execution plan and document through a REST API.

The agent must demonstrate reasoning, planning, orchestration, and tool usage rather than acting as a simple prompt wrapper.

---

# Assignment Constraints

The implementation must satisfy all assignment requirements.

Mandatory capabilities include:

* FastAPI REST API
* POST /agent endpoint
* Natural language request processing
* Autonomous task planning
* Sequential task execution
* Microsoft Word document generation
* One engineering improvement

The chosen engineering improvement is:

**Reflection / Self-Check**

The agent must review its own generated content before producing the final document.

---

# Design Philosophy

The project should follow the following principles.

## Simplicity

Avoid unnecessary frameworks.

Do not introduce technologies unless they provide measurable value.

The implementation should remain understandable by a single engineer.

---

## Modularity

Every module should have one responsibility.

Examples:

Planner
→ planning only

Executor
→ execution only

Reflector
→ quality checking only

Document Generator
→ Word document generation only

No module should perform multiple unrelated responsibilities.

---

## Explainability

Every architectural decision should be explainable during the interview.

If a component cannot be justified from an engineering perspective, it should not be included.

---

## Extensibility

The system should be designed so future improvements require minimal modification.

Examples:

* Replace Groq with another LLM
* Replace DOCX with PDF generation
* Add additional tools
* Replace single-agent with multi-agent architecture

without significant refactoring.

---

# High-Level Architecture

User Request

↓

Request Validation

↓

Planner

↓

Execution Engine

↓

Reflection

↓

Document Generator

↓

API Response

The system processes requests sequentially.

Each stage has a clearly defined responsibility.

---

# Selected Architecture

The implementation will use a **single autonomous agent with modular components**.

The system is intentionally not implemented as a multi-agent architecture.

Reasoning:

Advantages

* Simpler orchestration
* Easier debugging
* Faster implementation
* Lower token consumption
* Easier explanation during interview
* Better suited to the assignment time limit

Tradeoff

The architecture is less scalable than a true multi-agent system.

However, responsibilities remain separated into independent modules, allowing future migration if required.

---

# Technology Stack

Programming Language

Python 3.11+

API Framework

FastAPI

Server

Uvicorn

Validation

Pydantic

LLM Provider

Groq

Recommended Model

llama-3.3-70b-versatile

Document Generation

python-docx

Configuration

python-dotenv

Logging

Python logging module

Package Manager

pip

Version Control

Git

No database is required for this assignment.

No frontend is required.

---

# Project Structure

```text
autonomous-agent/

app.py
config.py
requirements.txt

agent/
    llm.py
    planner.py
    executor.py
    reflector.py
    prompts.py

models/
    schemas.py

tools/
    doc_generator.py

output/

docs/

prompts/
```

Every file must have a single responsibility.

No business logic should exist inside app.py.

---

# System Workflow

Step 1

Receive request

↓

Step 2

Validate request

↓

Step 3

Generate execution plan

↓

Step 4

Execute each task

↓

Step 5

Collect generated sections

↓

Step 6

Run reflection

↓

Step 7

Generate missing sections if necessary

↓

Step 8

Generate Word document

↓

Step 9

Return API response

---

# API Specification

Endpoint

POST /agent

Content-Type

application/json

Example Request

```json
{
  "request": "Create a project proposal for an AI customer support chatbot."
}
```

Example Response

```json
{
  "status": "completed",
  "plan": [
    "Understand project requirements",
    "Write executive summary",
    "Generate timeline",
    "Generate risk assessment",
    "Create implementation roadmap"
  ],
  "document_path": "output/project_proposal.docx"
}
```

Responses must always be valid JSON.

Unexpected exceptions must never expose internal stack traces to API users.

---

# Core Components

The system consists of five primary modules.

1. Planner

Responsible for understanding the user's request and converting it into an executable task list.

Input:

Natural language request.

Output:

Structured JSON task plan.

The planner must never generate document content.

Its only responsibility is planning.

---

2. Executor

Responsible for executing tasks produced by the planner.

Each task is executed independently.

Generated content is stored in memory until document creation.

The executor must not perform planning.

---

3. Reflector

Responsible for evaluating generated content.

The reflector checks for:

* missing sections
* incomplete responses
* duplicated information
* poor document flow

If missing content is detected, the reflector requests additional generation before document creation.

Reflection must occur exactly once before generating the final document.

---

4. Document Generator

Responsible only for generating the Microsoft Word document.

The generator receives structured content and creates a professional document using python-docx.

No LLM calls are allowed inside this module.

---

5. LLM Client

Responsible for all communication with the language model.

The client should expose a simple interface that accepts:

* system prompt
* user prompt

and returns generated text.

No planning or execution logic should exist inside the LLM client.

## Component Specifications

This section defines the expected behavior of every system component.

Each component has one responsibility.

Components must remain loosely coupled and communicate through well-defined interfaces.

---

# Planner

## Responsibility

The Planner is responsible for transforming a natural language request into a structured execution plan.

The Planner **must not** generate document content.

Its only responsibility is determining **what needs to be done**.

---

## Input

Natural language request.

Example:

> Create a project proposal for an AI-powered customer support chatbot for a hospital. Include assumptions where information is missing.

---

## Output

The Planner must always return valid JSON.

Example:

```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Analyze Request",
      "description": "Understand the user's objective."
    },
    {
      "id": 2,
      "title": "Generate Executive Summary",
      "description": "Create a professional executive summary."
    },
    {
      "id": 3,
      "title": "Generate Timeline",
      "description": "Create an implementation timeline."
    },
    {
      "id": 4,
      "title": "Generate Risk Analysis",
      "description": "Identify major risks."
    },
    {
      "id": 5,
      "title": "Generate Conclusion",
      "description": "Write the closing section."
    }
  ]
}
```

---

## Planner Rules

The Planner should:

* break work into logical steps
* avoid duplicate tasks
* produce tasks in execution order
* create only business-relevant tasks
* create between 4–10 tasks depending on complexity
* make reasonable assumptions when the request is ambiguous

The Planner must never:

* generate paragraphs
* generate report content
* generate DOCX
* perform reflection

---

# Executor

## Responsibility

The Executor is responsible for completing every task produced by the Planner.

Execution is sequential.

Tasks must be completed one at a time.

---

## Execution Algorithm

For every task:

1. Read task.
2. Read original user request.
3. Read previously generated sections.
4. Generate current section.
5. Save generated output.
6. Continue to next task.

Pseudo-code:

```text
for task in tasks

    build context

    call LLM

    store result

end
```

---

## Context Rules

Every task receives:

* original request
* completed sections
* current task

This ensures consistency across the document.

---

## Output Format

Every completed task returns:

```json
{
  "title": "Executive Summary",
  "content": "..."
}
```

The Executor stores all completed sections until document generation.

---

# Reflection

## Purpose

Reflection is the mandatory engineering improvement.

The Reflector reviews generated content before document generation.

---

## Responsibilities

The Reflector should evaluate:

* missing sections
* repeated information
* logical flow
* inconsistent assumptions
* incomplete document structure

---

## Reflection Output

```json
{
  "approved": false,
  "missing": [
    "Budget",
    "Success Metrics"
  ]
}
```

---

## Reflection Rules

If:

approved == true

continue.

Otherwise:

Generate every missing section.

Run reflection again.

Maximum reflection attempts:

2

If still incomplete:

Return the best available version.

Never enter an infinite loop.

---

# Document Generator

## Responsibility

Generate a professional Microsoft Word document.

Input:

Structured sections.

Output:

One .docx file.

---

## Formatting Rules

Use:

Heading 1

Document title

Heading 2

Section titles

Normal

Paragraphs

Add page breaks only when necessary.

Avoid unnecessary styling.

Professional appearance is preferred over decorative formatting.

---

# LLM Client

The LLM client is the only component allowed to communicate with Groq.

Responsibilities:

* send prompts
* receive responses
* retry transient failures
* return text

The client must not contain planning logic.

The client must not contain business logic.

---

# Prompt Engineering Rules

Every prompt must define:

Role

Objective

Context

Constraints

Expected output

---

Example structure:

SYSTEM

"You are an autonomous planning agent."

USER

Create an execution plan.

Return JSON only.

---

All prompts must request structured output whenever possible.

---

# Coding Standards

Every module should contain:

* module docstring
* type hints
* descriptive variable names
* logging
* exception handling

Avoid:

* global variables
* duplicated code
* excessively long functions
* hidden side effects

Maximum recommended function length:

40 lines

---

# Logging

Use Python logging.

Log:

request received

planner started

planner completed

executor started

task completed

reflection completed

document generated

API response sent

Do not log API keys.

Do not log sensitive information.

---

# Error Handling

Expected failures include:

* invalid request
* LLM timeout
* malformed JSON
* document generation failure

Handle failures gracefully.

Return meaningful API responses.

Never expose stack traces to clients.

---

# Retry Strategy

Retry only transient LLM failures.

Maximum retries:

2

Use exponential backoff.

Do not retry validation failures.

---

# Request Validation

Reject requests when:

* request field missing
* request empty
* request exceeds configured size

Return HTTP 400 with a descriptive message.

---

# JSON Validation

Planner output must be validated using Pydantic.

If validation fails:

Retry planning once.

If still invalid:

Return an error indicating the planner could not generate a valid execution plan.

Never continue with malformed plans.

---

# Performance Goals

Typical execution:

Under 20 seconds.

Reflection:

Maximum 2 iterations.

Memory usage:

Minimal.

Avoid unnecessary intermediate files.

---

# Security

Never execute arbitrary Python code.

Never execute shell commands generated by the LLM.

Never allow file path manipulation from user input.

Treat all LLM output as untrusted until validated.

---

# Acceptance Criteria

The implementation is considered complete when:

✓ POST /agent accepts valid requests.

✓ Planner generates structured task lists.

✓ Executor completes every task.

✓ Reflection reviews generated content.

✓ Missing sections are regenerated when necessary.

✓ Professional DOCX document is created.

✓ API returns execution plan and document path.

✓ Logs clearly describe execution flow.

✓ Errors are handled gracefully.

✓ Code is modular and interview-ready.
