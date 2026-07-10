"""Integration tests for the Autonomous AI Engineer API."""

import os
import unittest
from fastapi.testclient import TestClient

from app import app
from config import config
from agent.llm import LLMClient

client = TestClient(app)


def has_working_api_key() -> bool:
    """Verify the Groq API key works by making a minimal call."""
    key = config.GROQ_API_KEY
    if not key or not key.startswith("gsk_"):
        return False
    try:
        llm = LLMClient()
        llm.generate("Say OK", "Reply with the word OK only.")
        return True
    except Exception:
        return False


class TestHealthCheck(unittest.TestCase):
    """Tests for the health check endpoint."""

    def test_health_returns_200(self):
        """GET / should return healthy status."""
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")


class TestRequestValidation(unittest.TestCase):
    """Tests that invalid requests return HTTP 400."""

    def test_empty_request(self):
        response = client.post("/agent", json={"request": ""})
        self.assertEqual(response.status_code, 400)

    def test_whitespace_request(self):
        response = client.post("/agent", json={"request": "   "})
        self.assertEqual(response.status_code, 400)

    def test_missing_request_field(self):
        response = client.post("/agent", json={})
        self.assertEqual(response.status_code, 400)

    def test_oversized_request(self):
        response = client.post("/agent", json={"request": "x" * 10001})
        self.assertEqual(response.status_code, 400)

    def test_valid_request_structure(self):
        """Valid request may return 500 if no API key, but not 400."""
        response = client.post("/agent", json={"request": "Create a brief memo"})
        self.assertNotEqual(response.status_code, 400)


@unittest.skipIf(not has_working_api_key(), "Requires a working Groq API key")
class TestAgentPipeline(unittest.TestCase):
    """End-to-end pipeline tests. Requires a valid Groq API key."""

    def _run_pipeline(self, request_text: str):
        """Run the full pipeline and validate response structure."""
        response = client.post("/agent", json={"request": request_text})
        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(data["status"], "completed")
        self.assertIsInstance(data["plan"], list)
        self.assertGreater(len(data["plan"]), 0)
        self.assertIsInstance(data["document_path"], str)
        self.assertTrue(data["document_path"].endswith(".docx"))
        self.assertTrue(os.path.exists(data["document_path"]))

        return data

    def test_standard_meeting_minutes(self):
        """Test Case 1: Standard request from ROADMAP.md."""
        data = self._run_pipeline(
            "Create meeting minutes for a weekly product planning meeting."
        )
        self.assertIn("Meeting", data["plan"][0])

    def tearDown(self):
        """Clean up generated documents after each test."""
        output_dir = config.OUTPUT_DIRECTORY
        if os.path.isdir(output_dir):
            for f in os.listdir(output_dir):
                if f.endswith(".docx"):
                    os.remove(os.path.join(output_dir, f))

    def test_complex_proposal(self):
        """Test Case 2: Complex request with constraints."""
        data = self._run_pipeline(
            "Create a proposal for an AI recruitment assistant. "
            "Budget under $20,000. Timeline three months. "
            "Make reasonable assumptions where information is missing."
        )
        plan_text = " ".join(data["plan"]).lower()
        self.assertTrue(
            "budget" in plan_text or "cost" in plan_text,
            f"Expected budget-related task in plan: {data['plan']}",
        )
        self.assertTrue(
            "timeline" in plan_text or "schedule" in plan_text or "implement" in plan_text or "milestone" in plan_text,
            f"Expected timeline-related task in plan: {data['plan']}",
        )
        self.assertTrue(
            "assumption" in plan_text or "requirement" in plan_text or "scope" in plan_text,
            f"Expected assumption/requirement-related task in plan: {data['plan']}",
        )
        self.assertTrue(
            "risk" in plan_text or "vendor" in plan_text or "assessment" in plan_text or "evaluat" in plan_text,
            f"Expected risk-related task in plan: {data['plan']}",
        )

    def test_reflection_fills_gaps(self):
        """Reflection should complete without error."""
        response = client.post(
            "/agent",
            json={"request": "Create a project proposal with budget and risks."},
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        plan_text = " ".join(data["plan"]).lower()
        self.assertIn("risk", plan_text)
        self.assertIn("budget", plan_text)


if __name__ == "__main__":
    unittest.main()
