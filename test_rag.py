from rag.loader import load_documents
from rag.splitter import split_documents
from rag.embeddings import get_embeddings
from rag.vector_store import create_vector_store


from rag.loader import load_all_documents

docs = load_all_documents(
    "data/pdfs"
)

chunks = split_documents(docs)


embeddings = get_embeddings()


db = create_vector_store(
    chunks,
    embeddings
)


print("RAG Database Created Successfully")