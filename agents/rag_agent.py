from rag.retriever import get_retriever
from llm.groq_client import ask_groq


def rag_agent(question):

    retriever = get_retriever()

    documents = retriever.invoke(question)

    context = "\n\n".join(
        [doc.page_content for doc in documents]
    )

    prompt = f"""
You are an AI Software Engineering Assistant.

Use ONLY the following documentation.

Context:

{context}

Question:

{question}

Answer clearly.
"""

    answer = ask_groq(prompt)

    sources = []

    for doc in documents:

        source = doc.metadata.get("source","Unknown")

        sources.append(source)

    return {

        "answer": answer,

        "sources": list(set(sources))
    }