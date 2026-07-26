from rag.embeddings import embeddings
from langchain_chroma import Chroma


def get_retriever():

    db = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings
    )

    retriever = db.as_retriever(
        search_kwargs={"k": 3}
    )

    return retriever