# Demo Script — Autonomous AI Engineer

This script walks through a complete demonstration of the Autonomous AI Engineer.
Estimated time: 2–3 minutes.

---

## Prerequisites

- Python virtual environment activated
- Dependencies installed (`pip install -r requirements.txt`)
- Valid Groq API key in `.env`

---

## Step 1 — Start the Server

```bash
uvicorn app:app --reload
```

Expected output:

```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

---

## Step 2 — Verify Health

```bash
curl http://localhost:8000/
```

Expected response:

```json
{"status":"healthy","service":"Autonomous AI Engineer"}
```

---

## Step 3 — Standard Demo (Meeting Minutes)

```bash
curl -X POST http://localhost:8000/agent ^
  -H "Content-Type: application/json" ^
  -d "{\"request\":\"Create meeting minutes for a weekly product planning meeting.\"}"
```

Expected response (~10–20 seconds):

```json
{
  "status": "completed",
  "plan": [
    "Meeting Title and Participants",
    "Agenda Overview",
    "Discussion Summary",
    "Action Items",
    "Next Meeting Date"
  ],
  "document_path": "output\\document_20260709_143022.docx"
}
```

Point out:
- The `plan` array shows the LLM-generated task list
- `status: "completed"` confirms success
- The `.docx` file was saved to the `output/` directory

---

## Step 4 — Open the Document

Navigate to the `output/` folder and open the generated `.docx` file.

Expected formatting:
- **Heading 1**: Document title (derived from the request)
- **Heading 2**: Each section title (matching plan tasks)
- **Normal**: Structured paragraphs under each heading

---

## Step 5 — Complex Demo (Proposal with Constraints)

```bash
curl -X POST http://localhost:8000/agent ^
  -H "Content-Type: application/json" ^
  -d "{\"request\":\"Create a proposal for an AI recruitment assistant. Budget under $20,000. Timeline within three months. Include assumptions where information is missing.\"}"
```

Expected response (~15–25 seconds):

```json
{
  "status": "completed",
  "plan": [
    "Executive Summary",
    "Project Scope",
    "Budget Breakdown",
    "Implementation Timeline",
    "Assumptions",
    "Risk Analysis",
    "Conclusion"
  ],
  "document_path": "output\\document_20260709_143115.docx"
}
```

Point out:
- Dynamic planning adapted to this specific request (Budget, Timeline, Assumptions, Risks all generated)
- Reflection may have detected and filled missing sections

---

## Step 6 — Error Handling Demo

### Empty request (expects HTTP 400):

```bash
curl -X POST http://localhost:8000/agent ^
  -H "Content-Type: application/json" ^
  -d "{\"request\":\"\"}"
```

Expected:

```json
{"detail":"Request cannot be empty"}
```

### Missing field (expects HTTP 400):

```bash
curl -X POST http://localhost:8000/agent ^
  -H "Content-Type: application/json" ^
  -d "{}"
```

Expected:

```json
{"detail":"request\n  Field required"}
```

---

## Talking Points

During the demo, highlight:

1. **Modular architecture** — Four independent modules (Planner, Executor, Reflector, DocGenerator) each with one responsibility
2. **Autonomous planning** — The LLM decides what tasks to create, not hardcoded
3. **Self-reflection** — The Reflector reviews content and fills gaps (max 2 cycles)
4. **Error resilience** — Retry logic for transient LLM failures, validation at every step
5. **Clean API** — Single endpoint, validated input, structured JSON response, no stack trace leaks
