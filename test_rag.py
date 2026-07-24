from rag.loader import load_documents
from rag.splitter import split_documents
from rag.embeddings import get_embeddings
from rag.vector_store import create_vector_store


docs = load_documents(
    "data/pdfs/python.pdf"
)


chunks = split_documents(docs)


embeddings = get_embeddings()


db = create_vector_store(
    chunks,
    embeddings
)


print("RAG Database Created Successfully")