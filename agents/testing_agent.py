from llm.groq_client import ask_groq


def testing_agent(question):

    prompt = f"""

You are a Software Testing Expert.

User Request:

{question}


Generate:

1. Test cases
2. Unit test explanation
3. pytest code
4. Edge cases
5. Best testing practices


Give a professional answer.

"""

    response = ask_groq(prompt)

    return response