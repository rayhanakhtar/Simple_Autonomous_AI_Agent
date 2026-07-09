# OPENCODE_INSTRUCTIONS.md

# OpenCode Implementation Instructions

Version: 1.0

---

# Purpose

This document defines how OpenCode should implement this project.

It supplements **AGENT.md** and **IMPLEMENTATION_GUIDE.md**.

If any conflict exists:

1. AGENT.md
2. IMPLEMENTATION_GUIDE.md
3. OPENCODE_INSTRUCTIONS.md

This priority order must always be respected.

---

# Overall Goal

Build a production-quality Python project demonstrating an autonomous AI agent capable of:

* Understanding a natural language request
* Creating its own execution plan
* Executing each task
* Reviewing its own work (Reflection)
* Producing a professional Microsoft Word (.docx) document
* Exposing everything through a FastAPI REST API

The implementation should prioritize clarity, modularity, and interview readiness over unnecessary sophistication.

---

# General Rules

Always write code as if it will be reviewed by a senior Python engineer.

Every file should be readable.

Every class should have one responsibility.

Every function should have one purpose.

Avoid clever code.

Prefer maintainability.

---

# Coding Standards

Always include:

* module docstrings
* function docstrings
* type hints
* descriptive variable names
* logging
* exception handling

Never:

* use wildcard imports
* duplicate logic
* hardcode API keys
* suppress exceptions silently
* place unrelated responsibilities inside one module

---

# Project Organization

Follow exactly the folder structure defined in **AGENT.md**.

Do not create additional frameworks or directories unless absolutely necessary.

Do not introduce unnecessary abstractions.

---

# Implementation Order

Implement modules in this exact order.

1. Configuration
2. Pydantic schemas
3. LLM client
4. Prompt templates
5. Planner
6. Executor
7. Reflector
8. DOCX generator
9. FastAPI endpoint
10. Integration testing

Complete one module before moving to the next.

Do not leave placeholder implementations.

---

# Planner Instructions

The planner is responsible only for planning.

Never generate document content inside the planner.

The planner must always return structured JSON.

Validate the planner output before returning.

If validation fails:

Retry once.

If validation fails again:

Return a meaningful error.

---

# Executor Instructions

Execute tasks sequentially.

Never skip tasks.

Each task should receive:

* original request
* previous sections
* current task description

Store generated sections in memory until reflection is complete.

---

# Reflection Instructions

Reflection is mandatory.

The reflector should review:

* completeness
* duplicated content
* logical flow
* missing sections

If sections are missing:

Generate only the missing sections.

Maximum review cycles:

2

Never enter recursive or infinite loops.

---

# DOCX Generator Instructions

Use `python-docx`.

The document should include:

* title
* headings
* paragraphs

Use built-in Word styles.

Do not add unnecessary formatting.

Keep the document professional.

---

# FastAPI Instructions

Expose:

POST /agent

Accept:

```json
{
  "request": "..."
}
```

Return:

```json
{
  "status": "completed",
  "plan": [...],
  "document_path": "..."
}
```

Use Pydantic request and response models.

---

# Logging Requirements

Log major milestones.

Examples:

* Request received
* Planner started
* Planner completed
* Executor started
* Task completed
* Reflection completed
* Document generated
* Response returned

Never log secrets.

---

# Error Handling

Handle:

* invalid requests
* invalid planner JSON
* LLM failures
* document generation failures

Return meaningful HTTP responses.

Never expose internal stack traces.

---

# Dependencies

Prefer only the following libraries:

* FastAPI
* Uvicorn
* Pydantic
* python-dotenv
* groq
* python-docx

Avoid unnecessary third-party dependencies.

Keep the project lightweight.

---

# Prompt Engineering

Store prompts separately.

Do not embed large prompt strings inside business logic.

Prompt templates belong in `agent/prompts.py`.

Each prompt should clearly define:

* role
* objective
* context
* constraints
* expected output format

---

# Code Quality Expectations

Functions should generally remain under 40 lines where practical.

Prefer helper functions over deeply nested logic.

Avoid excessive inheritance.

Favor composition.

---

# Documentation

Every public class should include a docstring.

Every public function should include:

* purpose
* parameters
* return value

Keep comments focused on explaining *why*, not *what*.

---

# Security

Treat all LLM output as untrusted.

Validate planner JSON.

Never execute arbitrary code from model responses.

Never execute shell commands suggested by the model.

Never trust file paths from user input.

---

# Assignment Focus

Remember that this project is an engineering assignment.

Prioritize:

* clean architecture
* modularity
* readability
* explainability
* robustness

Do not optimize for maximum features.

Optimize for demonstrating engineering thinking.

---

# Explicitly Out of Scope

Do not implement unless explicitly requested:

* authentication
* databases
* background workers
* Docker
* frontend
* RAG
* memory
* multi-agent orchestration
* external business APIs

Keep the MVP focused.

---

# Final Validation Checklist

Before considering the implementation complete, verify:

* [ ] FastAPI application starts successfully.
* [ ] `/agent` endpoint accepts valid requests.
* [ ] Planner produces valid JSON tasks.
* [ ] Executor completes all planned tasks.
* [ ] Reflection executes and improves output when needed.
* [ ] `.docx` document is generated successfully.
* [ ] API returns the execution plan and document path.
* [ ] Logs are informative.
* [ ] Exceptions are handled gracefully.
* [ ] Code is modular and easy to explain in an interview.

The finished project should resemble production-quality engineering code rather than a proof-of-concept or prototype.
