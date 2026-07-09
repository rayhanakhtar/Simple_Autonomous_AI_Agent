# docs/architecture.md

# Autonomous AI Engineer

## System Architecture

Version: 1.0

---

# Overview

The Autonomous AI Engineer is designed as a **modular single-agent system**.

The objective is to transform a natural language business request into a professional Microsoft Word document through autonomous planning, sequential execution, self-reflection, and document generation.

The architecture follows the principles of:

* Single Responsibility
* Separation of Concerns
* Low Coupling
* High Cohesion
* Explainability
* Extensibility

---

# High-Level Architecture

```text
                    User
                     │
                     ▼
              FastAPI Endpoint
                     │
                     ▼
           Request Validation
                     │
                     ▼
                  Planner
                     │
                     ▼
             Execution Plan
                     │
                     ▼
                 Executor
                     │
                     ▼
          Generated Sections
                     │
                     ▼
                Reflector
             ┌──────────────┐
             │ Approved ?   │
             └──────┬───────┘
                    │
          Yes       │      No
           │        │
           ▼        ▼
      DOCX Tool   Missing Sections
           ▲        │
           └────────┘
                │
                ▼
          API Response
```

---

# Component Responsibilities

## FastAPI

Responsibilities

* Receive requests
* Validate input
* Coordinate modules
* Return responses

Must never contain business logic.

---

## Planner

Responsibilities

* Understand the request
* Produce execution plan
* Return validated JSON

Must never generate document content.

---

## Executor

Responsibilities

* Execute one task at a time
* Maintain execution context
* Generate document sections

Must never perform planning.

---

## Reflector

Responsibilities

* Evaluate completeness
* Detect missing sections
* Trigger regeneration

Must never rewrite the full document.

---

## Document Generator

Responsibilities

* Format content
* Generate Word document
* Save file
* Return path

Must never call the LLM.

---

## LLM Client

Responsibilities

* Handle Groq communication
* Retry transient failures
* Return model output

Must not contain business logic.

---

# Request Lifecycle

```text
POST /agent

↓

Validate Request

↓

Planner

↓

Task List

↓

Executor

↓

Document Sections

↓

Reflection

↓

Generate Missing Sections (if required)

↓

DOCX Generator

↓

Return Response
```

Every request follows exactly this lifecycle.

---

# Data Flow

The system exchanges structured objects rather than raw strings whenever possible.

```text
AgentRequest
        │
        ▼
Planner
        │
        ▼
List[Task]
        │
        ▼
Executor
        │
        ▼
List[DocumentSection]
        │
        ▼
Reflector
        │
        ▼
ReflectionResult
        │
        ▼
DocumentGenerator
        │
        ▼
AgentResponse
```

Using typed models improves readability, validation, and maintainability.

---

# Internal Models

Core objects include:

* AgentRequest
* Task
* ExecutionContext
* DocumentSection
* ReflectionResult
* AgentResponse

These objects form the contract between components.

No module should exchange loosely structured dictionaries unless interacting directly with the LLM.

---

# Dependency Graph

```text
app.py
│
├── Planner
│      │
│      └── LLMClient
│
├── Executor
│      │
│      └── LLMClient
│
├── Reflector
│      │
│      └── LLMClient
│
└── DocumentGenerator
```

There should be no circular dependencies.

The LLM client is a shared infrastructure component.

---

# Reflection Cycle

```text
Planner
      │
      ▼
Executor
      │
      ▼
Reflector
      │
      ▼
Approved?
   │        │
 Yes        No
   │        │
   ▼        ▼
 Finish   Generate Missing Sections
              │
              ▼
         Reflect Once More
```

Maximum reflection iterations: **2**.

This prevents infinite regeneration loops while still demonstrating autonomous self-correction.

---

# Error Handling Strategy

Validation Error

→ HTTP 400

Planner JSON Error

→ Retry once

LLM Failure

→ Retry with exponential backoff

Reflection Failure

→ Continue with the best available output

Document Generation Failure

→ HTTP 500

Unexpected Error

→ Generic error response without exposing internal details

---

# Logging Strategy

Log only significant events:

* Request received
* Planning started
* Planning completed
* Task execution started
* Task completed
* Reflection completed
* Document generated
* Response returned

Sensitive information such as API keys must never be logged.

---

# Design Principles

The implementation follows these principles:

## Single Responsibility

Every module has one clear responsibility.

## Composition Over Inheritance

Components collaborate through well-defined interfaces rather than deep inheritance hierarchies.

## Structured Data

Use Pydantic models internally whenever possible.

Avoid untyped dictionaries.

## Explicit Contracts

Every component exposes a small public interface with predictable inputs and outputs.

## Fail Gracefully

Recover from transient failures where practical.

Return meaningful errors otherwise.

---

# Non-Functional Requirements

Maintainability

The codebase should be understandable by another engineer without extensive explanation.

Extensibility

Components should be replaceable with minimal changes.

Reliability

The system should handle malformed requests and transient LLM failures gracefully.

Performance

Typical request execution should complete within approximately 20 seconds, depending on LLM latency.

---

# Future Evolution

The architecture is intentionally modular so that future improvements can be introduced without major refactoring.

Potential enhancements include:

* Multi-agent orchestration
* Retrieval-Augmented Generation (RAG)
* Conversation memory
* Tool calling
* Persistent storage
* Asynchronous execution
* Background job processing
* Additional export formats (PDF, HTML)

These enhancements are deliberately excluded from the MVP to keep the implementation aligned with the assignment's scope while providing a clear migration path for future development.
