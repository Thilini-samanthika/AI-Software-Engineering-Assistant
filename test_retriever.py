from rag.retriever import get_retriever

retriever = get_retriever()

results = retriever.invoke("Explain SOLID Principles")

print("Number of Documents:", len(results))

for i, doc in enumerate(results, start=1):

    print("\n========================")
    print(f"Document {i}")
    print("Source :", doc.metadata.get("source", "Unknown"))
    print("------------------------")
    print(doc.page_content[:500])