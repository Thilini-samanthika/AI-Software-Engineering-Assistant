from langchain_chroma import Chroma
from rag.embeddings import embeddings


def search_uploaded_pdf(question):

    db = Chroma(

        persist_directory="uploaded_db",

        embedding_function=embeddings

    )

    docs = db.similarity_search(

        question,

        k=4

    )

    return docs