from llm.groq_client import ask_groq


def coding_agent(question: str):

    prompt = f"""
You are an expert Software Engineer.

Your job is to:

- Explain code
- Find bugs
- Suggest fixes
- Improve code quality
- Explain algorithms

User Question:

{question}
"""

    return ask_groq(prompt)