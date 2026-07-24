from rag.retriever import get_retriever


retriever = get_retriever()


results = retriever.invoke(
    "Explain Python programming"
)


print("Number of Documents:", len(results))


for i, doc in enumerate(results):

    print("\n====================")
    print("Document", i+1)

    print(doc.page_content[:500])