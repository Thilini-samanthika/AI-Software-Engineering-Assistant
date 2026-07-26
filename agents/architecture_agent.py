from llm.groq_client import ask_groq


def architecture_agent(question):

    prompt = f"""

You are a Software Architect.

Question:

{question}


Provide:

1. System Architecture
2. Design Patterns
3. Folder Structure
4. Database Design
5. Technology Recommendation
6. Scalability Suggestions


Answer professionally.

"""


    response = ask_groq(prompt)

    return response