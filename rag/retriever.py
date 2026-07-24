from rag.embeddings import get_embeddings
from langchain_chroma import Chroma


def get_retriever():

    embeddings = get_embeddings()

    db = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings
    )

    retriever = db.as_retriever(
        search_kwargs={
            "k": 3
        }
    )

    return retriever