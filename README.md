# Autonomous AI Engineer

An autonomous AI agent built with **FastAPI** and **Groq** that understands natural language requests, creates an execution plan, executes tasks sequentially, performs self-reflection, and generates professional Microsoft Word (`.docx`) business documents.

---

## Features

- **Autonomous Planning** — Analyzes a natural language request and generates a structured execution plan (4–10 tasks) using an LLM.
- **Sequential Task Execution** — Executes each planned task independently, maintaining context from previously generated sections.
- **Self-Reflection** — Reviews generated content for missing sections, logical flow, and completeness. Automatically regenerates gaps (max 2 cycles).
- **Professional DOCX Generation** — Produces a formatted Word document with headings and structured sections using `python-docx`.
- **REST API** — Single `POST /agent` endpoint with JSON request/response.
- **Robust Error Handling** — Retry with exponential backoff for transient LLM failures, Pydantic request validation, and graceful error responses (never exposes stack traces).

---

## Architecture

```
                  User Request
                       |
                       v
              Request Validation
                       |
                       v
                 Planner (LLM)
                       |
                       v
            Sequential Executor
                       |
                       v
           Reflection / Self-Check
              /              \
         Approved        Missing Sections
             |                 |
             v                 v
      DOCX Generator     Executor (re-run)
             |                 |
             +--------+--------+
                      |
                      v
                API Response
```

---

## Project Structure

```
Simple_Autonomous_AI_Agent/
│
├── app.py                    # FastAPI entry point, routes, orchestration
├── config.py                 # Environment config, validation, constants
├── requirements.txt          # Pinned Python dependencies
├── .env.example              # Environment variable template
├── .gitignore
│
├── agent/
│   ├── __init__.py           # Package exports (LLMClient, Planner, Executor, Reflector)
│   ├── llm.py                # LLMClient — Groq communication with retry logic
│   ├── planner.py            # Planner — creates execution plan from request
│   ├── executor.py           # Executor — executes tasks sequentially
│   ├── reflector.py          # Reflector — reviews content, fills gaps
│   └── prompts.py            # Prompt templates for planner, executor, reflector
│
├── models/
│   ├── __init__.py
│   └── schemas.py            # Pydantic models: AgentRequest, Task, DocumentSection, etc.
│
├── tools/
│   ├── __init__.py
│   └── doc_generator.py      # create_document() — generates .docx from sections
│
├── prompts/                  # Prompt specification documents
│   ├── planner.md
│   ├── executor.md
│   └── reflector.md
│
├── docs/
│   ├── architecture.md       # System architecture documentation
│   └── demo.md               # Step-by-step demo script
│
├── output/                   # Generated .docx files (gitignored)
│
├── AGENT.md                  # Master system specification
├── IMPLEMENTATION_GUIDE.md   # Implementation blueprint
├── OPENCODE_INSTRUCTIONS.md  # Coding rules
├── ROADMAP.md                # Phase-by-phase implementation plan
├── DECISIONS.md              # Architecture Decision Records
└── test_agent.py             # Integration test suite
```

---

## Technology Stack

| Component           | Technology              |
| ------------------- | ----------------------- |
| Language            | Python 3.11+            |
| API Framework       | FastAPI                 |
| Server              | Uvicorn                 |
| LLM Provider        | Groq                    |
| Model               | `llama-3.3-70b-versatile` |
| Validation          | Pydantic                |
| Document Generation | python-docx             |
| Configuration       | python-dotenv           |
| Testing             | pytest                  |
| Logging             | Python logging          |

---

## Quickstart

### Prerequisites

- Python 3.11+
- A [Groq API key](https://console.groq.com/keys) (free tier available)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd Simple_Autonomous_AI_Agent

# Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate    # Windows
# source .venv/bin/activate  # Linux / macOS

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
```

### Configuration

Edit `.env` with your Groq API key:

```env
GROQ_API_KEY=gsk_your_api_key_here
MODEL_NAME=llama-3.3-70b-versatile
OUTPUT_DIRECTORY=output
MAX_RETRIES=2
MAX_REQUEST_LENGTH=10000
LOG_LEVEL=INFO
```

| Variable             | Description                            | Default                      |
| -------------------- | -------------------------------------- | ---------------------------- |
| `GROQ_API_KEY`       | Your Groq API key (required)           | —                            |
| `MODEL_NAME`         | LLM model to use                       | `llama-3.3-70b-versatile`    |
| `OUTPUT_DIRECTORY`   | Directory for generated documents      | `output`                     |
| `MAX_RETRIES`        | Max retry attempts for transient LLM failures | `2`                    |
| `MAX_REQUEST_LENGTH` | Max characters in a user request       | `10000`                      |
| `LOG_LEVEL`          | Logging level (DEBUG, INFO, WARNING, ERROR) | `INFO`                  |

### Run the Server

```bash
uvicorn app:app --reload
```

The API will be available at `http://localhost:8000`.

---

## API

### Health Check

```http
GET /
```

```json
{
  "status": "healthy",
  "service": "Autonomous AI Engineer"
}
```

### Generate Document

```http
POST /agent
Content-Type: application/json
```

#### Request Body

| Field     | Type   | Required | Description          |
| --------- | ------ | -------- | -------------------- |
| `request` | string | Yes      | Natural language request (1–10000 characters) |

```json
{
  "request": "Create a project proposal for an AI customer support chatbot."
}
```

#### Success Response (200)

```json
{
  "status": "completed",
  "plan": [
    "Analyze requirements",
    "Generate executive summary",
    "Define project scope",
    "Generate implementation timeline",
    "Identify risks",
    "Create conclusion"
  ],
  "document_path": "output\\document_20260709_143022.docx"
}
```

| Field           | Type   | Description                              |
| --------------- | ------ | ---------------------------------------- |
| `status`        | string | `"completed"` or `"error"`               |
| `plan`          | array  | Ordered list of task titles              |
| `document_path` | string | Path to the generated `.docx` file       |

#### Error Responses

| Status | Description               |
| ------ | ------------------------- |
| 400    | Invalid or empty request  |
| 500    | Internal processing error |

---

## Testing

The test suite (`test_agent.py`) contains 9 integration tests:

### Always-Run Tests (6)

| Test                              | What It Verifies                          |
| --------------------------------- | ----------------------------------------- |
| `test_health_check`               | `GET /` returns healthy status            |
| `test_request_empty`              | Rejects empty request body                |
| `test_request_whitespace`         | Rejects whitespace-only request           |
| `test_request_missing_field`      | Rejects JSON without `request` field      |
| `test_request_oversized`          | Rejects requests exceeding max length     |
| `test_request_valid_structure`    | Accepts a valid well-formed request       |

### Pipeline Tests (3, require valid Groq API key)

| Test                              | What It Verifies                          |
| --------------------------------- | ----------------------------------------- |
| `test_standard_meeting_minutes`   | Full pipeline: plan → execute → reflect → docx |
| `test_complex_proposal`           | Complex request with budget, timeline, risks, assumptions |
| `test_reflection_fills_gaps`      | Reflection correctly identifies and fills missing sections |

Run all tests:

```bash
pytest test_agent.py -v
```

Run validation tests only (no API key needed):

```bash
pytest test_agent.py -v -k "not pipeline"
```

---

## How It Works

1. **Request Validation** — The API validates the incoming request (non-empty, within size limits).
2. **Planning** — The `Planner` sends the request to Groq's `llama-3.3-70b-versatile` and receives a structured JSON task list (validated with Pydantic).
3. **Execution** — The `Executor` processes each task sequentially. For each task, it sends the original request, previously generated sections, and the current task description to the LLM, then stores the result as a `DocumentSection`.
4. **Reflection** — The `Reflector` evaluates the generated content for completeness, logical flow, and missing sections. If gaps are found, it generates missing content (max 2 cycles).
5. **Document Generation** — The `doc_generator` creates a `.docx` file with Heading 1 for the document title, Heading 2 for sections, and Normal style for paragraphs.
6. **Response** — The API returns the execution plan and the path to the generated document.

---

## Example Test Cases

### Standard Request

```
Input:  "Create meeting minutes for a weekly product planning meeting."
Output: .docx file with structured meeting minutes
```

### Complex Request

```
Input:  "Create a proposal for an AI recruitment assistant. Budget under $20,000. Timeline within three months. Include assumptions where information is missing."
Output: .docx file with executive summary, budget, timeline, risks, assumptions
```

---

## Engineering Decisions

- **Single-agent modular architecture** — Simplifies orchestration while maintaining separation of concerns (Planning, Execution, Reflection, Document Generation).
- **Reflection as mandatory improvement** — Demonstrates autonomous quality control without significant complexity. Max 2 cycles to prevent infinite loops.
- **Pydantic validation on all structured LLM output** — Ensures malformed JSON never propagates through the pipeline.
- **Retry with exponential backoff** — Handles transient LLM failures (rate limits, timeouts, server errors) without failing the entire request.
- **Prompts stored separately** — All prompt templates in `agent/prompts.py` for easy iteration without touching business logic.

---

## Future Improvements

- Multi-agent architecture
- Retrieval-Augmented Generation (RAG)
- Conversation memory
- Tool calling with external APIs
- Streaming responses
- PDF generation
- Docker support
- Persistent storage
- Async execution
- Web interface

---

## License

This project was created for educational and interview demonstration purposes.
