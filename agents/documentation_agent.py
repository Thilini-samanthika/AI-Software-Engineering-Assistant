from llm.groq_client import ask_groq


def documentation_agent(question: str):

    prompt = f"""
You are a Technical Documentation Expert.

Generate:

- README
- API Documentation
- Function Comments
- Markdown Documentation

User Request:

{question}
"""

    return ask_groq(prompt)