from llm.groq_client import ask_groq


def code_review_agent(question):


    prompt = f"""

You are an Expert Code Reviewer.


Analyze this code:


{question}


Review:

1. Bugs
2. Security Issues
3. Performance
4. SOLID violations
5. Code Quality
6. Improvements


Provide suggestions.

"""


    response = ask_groq(prompt)

    return response