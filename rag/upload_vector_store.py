from langchain_chroma import Chroma
from rag.embeddings import embeddings


def get_retriever():
    
    db = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings
    )

    retriever = db.as_retriever(
        search_kwargs={"k": 3}
    )

    return retriever


def get_uploaded_vector_store():
    
    db = Chroma(
        persist_directory="uploaded_db",
        embedding_function=embeddings
    )
    return db


def create_uploaded_vector_db(chunks, embedding_function=None):
   
    db = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_function or embeddings,
        persist_directory="uploaded_db"
    )
    return db