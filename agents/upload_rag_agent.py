from rag.upload_retriever import search_uploaded_pdf
from llm.groq_client import ask_groq


def upload_rag_agent(question):

    docs = search_uploaded_pdf(question)

    context = ""

    sources = []


    for doc in docs:

        context += doc.page_content + "\n\n"

        sources.append(

            doc.metadata["source"]

        )


    prompt = f"""

Answer using ONLY this document.

Context:

{context}

Question:

{question}

"""

    answer = ask_groq(prompt)


    return {

        "answer": answer,

        "sources": sources

    }