
import logging
import re

from llm.groq_client import ask_groq

logger = logging.getLogger(__name__)

VALID_AGENTS = {
    "coding",
    "documentation",
    "rag",
    "testing",
    "architecture",
    "code_review",
    "upload_rag",
}

KEYWORDS = {
    "upload_rag": [
        "uploaded", "uploaded pdf", "my pdf",
        "this document", "this pdf",
        "uploaded document",
        "attached file", "attached pdf",
        "my uploaded file",
    ],
    "testing": [
        "unit test", "pytest", "test case",
        "testing", "test code", "generate test",
        "automation test", "automated test",
        "tdd", "write tests",
    ],
    "architecture": [
        "architecture", "system design",
        "system architecture", "design system",
        "folder structure", "software architecture",
        "database design", "scalable system",
        "microservices",
    ],
    "code_review": [
        "review code", "code review",
        "review my code", "review this code",
        "review this python code",
        "review the code",
        "review the following code",
        "review this function",
        "identify issues", "find issues",
        "improve code", "code quality",
        "clean code", "solid violation",
        "security issue", "performance issue",
    ],
    "documentation": [
        "readme", "documentation", "api docs",
        "api documentation", "docstring",
        "project document", "write comments",
        "generate comments",
    ],
    "coding": [
        "code", "python", "java", "c#",
        "bug", "debug", "error", "exception",
        "fix", "algorithm", "optimize",
        "function", "class", "loop",
        "array", "string",
    ],
    "rag": [
        "solid", "oop", "design pattern",
        "git", "github", "sql", "docker",
        "kubernetes", "rest api", "agile",
        "scrum", "refactoring",
        "dependency injection",
    ],
}


def contains_keyword(text: str, keyword: str) -> bool:
    pattern = (
        r"(?<!\w)"
        + re.escape(keyword)
        + r"(?!\w)"
    )
    return re.search(pattern, text) is not None


def router_agent(question: str) -> str:
    """Route a request to one supported agent."""

    if not isinstance(question, str):
        return "rag"

    question_lower = question.lower().strip()

    if not question_lower:
        return "rag"

    # Explicit requests take priority over generic
    # programming keywords.
    for agent, keywords in KEYWORDS.items():
        for keyword in keywords:
            if contains_keyword(question_lower, keyword):
                logger.info("Router selected: %s", agent)
                return agent

    prompt = f"""
You are a software engineering AI router.

Classify the request into exactly ONE category:

coding
documentation
rag
testing
architecture
code_review
upload_rag

Rules:
- coding: Write, explain, or debug code.
- documentation: README, docstrings, API docs.
- testing: Generate or explain tests.
- architecture: System design and structure.
- code_review: Review existing code for issues.
- rag: Software engineering concepts.
- upload_rag: Questions about uploaded files.

Return ONLY the category name.

User request:
{question}
"""

    try:
        response = ask_groq(prompt).strip().lower()

        if response in VALID_AGENTS:
            logger.info("AI Router selected: %s", response)
            return response

        logger.warning(
            "Unexpected router response: %s",
            response[:100],
        )

    except Exception:
        logger.exception("AI Router failed")

    return "rag"
