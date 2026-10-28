
import pytest
from agents.router import router_agent


@pytest.mark.parametrize(
    "question, expected",
    [
        ("Review this Python code and identify issues", "code_review"),
        ("Generate pytest unit tests", "testing"),
        ("Create a system architecture", "architecture"),
        ("Write API documentation", "documentation"),
        ("Write a Python function", "coding"),
        ("Explain SOLID principles", "rag"),
        ("Summarize my uploaded PDF", "upload_rag"),
    ],
)
def test_agent_routing(question, expected):
    assert router_agent(question) == expected
