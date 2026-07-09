# Autonomous AI Engineer – Autonomous Planning Agent

> An autonomous AI agent built with FastAPI and Groq that understands natural language requests, creates its own execution plan, executes tasks sequentially, performs self-reflection, and generates professional Microsoft Word (.docx) business documents.

---

## Project Overview

This project was developed as part of an **Autonomous AI Engineer Build Challenge**.

The objective was to design and implement an AI agent capable of performing end-to-end autonomous task execution rather than acting as a simple chatbot.

The agent demonstrates:

* Autonomous planning
* Multi-step reasoning
* Task orchestration
* Reflection / Self-check
* Tool usage
* REST API design
* Professional document generation

The implementation prioritizes software engineering principles including modular architecture, separation of concerns, readability, and maintainability.

---

# Features

### Autonomous Planning

The agent analyzes a natural language request and creates its own execution plan.

Example:

User Request

> Create a project proposal for an AI customer support chatbot.

Generated Plan

1. Analyze requirements
2. Generate executive summary
3. Define project scope
4. Generate implementation timeline
5. Identify risks
6. Create conclusion

---

### Sequential Task Execution

Each planned task is executed independently.

Every generated section is stored before assembling the final document.

---

### Reflection / Self-Check

Before generating the final document, the system evaluates its own output.

The reflection module checks for:

* Missing sections
* Logical flow
* Repeated content
* Incomplete structure

Missing content is automatically generated before document creation.

---

### Professional DOCX Generation

The final output is generated as a Microsoft Word document using **python-docx**.

Documents are professionally formatted using headings and structured sections.

---

### REST API

The project exposes a FastAPI endpoint.

```http
POST /agent
```

Request

```json
{
    "request": "Create a business proposal for an AI HR assistant."
}
```

Response

```json
{
    "status": "completed",
    "plan": [
        "...",
        "..."
    ],
    "document_path": "output/proposal.docx"
}
```

---

# Architecture

```text
                User Request
                      │
                      ▼
             Request Validation
                      │
                      ▼
                Planner (LLM)
                      │
                      ▼
            Sequential Executor
                      │
                      ▼
           Reflection / Self-Check
                      │
                      ▼
            DOCX Generation Tool
                      │
                      ▼
                FastAPI Response
```

---

# Project Structure

```text
autonomous-agent/
│
├── app.py
├── config.py
├── requirements.txt
│
├── agent/
│   ├── llm.py
│   ├── planner.py
│   ├── executor.py
│   ├── reflector.py
│   └── prompts.py
│
├── models/
│   └── schemas.py
│
├── tools/
│   └── doc_generator.py
│
├── docs/
│
├── prompts/
│
└── output/
```

---

# Technology Stack

| Component           | Technology              |
| ------------------- | ----------------------- |
| Language            | Python 3.11+            |
| API                 | FastAPI                 |
| LLM                 | Groq                    |
| Model               | llama-3.3-70b-versatile |
| Validation          | Pydantic                |
| Document Generation | python-docx             |
| Configuration       | python-dotenv           |
| Logging             | Python logging          |

---

# Installation

Clone the repository.

```bash
git clone <repository-url>
```

Create a virtual environment.

```bash
python -m venv .venv
```

Activate the environment.

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

Create a `.env` file.

```text
GROQ_API_KEY=your_api_key
MODEL_NAME=llama-3.3-70b-versatile
```

Start the server.

```bash
uvicorn app:app --reload
```

---

# API

## Endpoint

```http
POST /agent
```

### Request

```json
{
    "request":"Create a proposal for an AI recruitment assistant."
}
```

### Response

```json
{
    "status":"completed",
    "plan":[
        "...",
        "..."
    ],
    "document_path":"output/proposal.docx"
}
```

---

# Example Test Cases

## Standard Request

```
Create meeting minutes for a weekly product planning meeting.
```

Expected Behavior

* Generate execution plan
* Execute tasks
* Review content
* Generate DOCX

---

## Complex Request

```
Create a proposal for an AI recruitment assistant.

Budget under $20,000.

Timeline within three months.

Include assumptions where information is missing.
```

Expected Behavior

* Dynamic planning
* Assumption generation
* Timeline creation
* Budget planning
* Risk analysis
* Reflection
* DOCX generation

---

# Engineering Decisions

The project intentionally uses a **single-agent modular architecture**.

This minimizes orchestration complexity while still demonstrating:

* Planning
* Reasoning
* Sequential execution
* Reflection
* Tool orchestration

Reflection was selected as the mandatory engineering improvement because it demonstrates autonomous quality control without significantly increasing implementation complexity.

---

# Future Improvements

Potential enhancements include:

* Multi-agent architecture
* Retrieval-Augmented Generation (RAG)
* Conversation memory
* Tool calling
* Streaming responses
* PDF generation
* Docker support
* Persistent storage
* Async execution
* Web interface

---

# Assignment Requirements Mapping

| Requirement               | Status |
| ------------------------- | ------ |
| FastAPI API               | ✅      |
| Natural Language Requests | ✅      |
| Autonomous Planning       | ✅      |
| Sequential Task Execution | ✅      |
| Reflection / Self-Check   | ✅      |
| DOCX Generation           | ✅      |
| Free LLM                  | ✅      |
| REST API                  | ✅      |
| Structured Output         | ✅      |

---

# License

This project was created for educational and interview demonstration purposes.
