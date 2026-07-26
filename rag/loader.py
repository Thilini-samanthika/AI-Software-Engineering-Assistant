import os

from langchain_community.document_loaders import PyPDFLoader


def load_all_documents(folder):

    documents = []

    for root, dirs, files in os.walk(folder):

        for file in files:

            if file.endswith(".pdf"):

                path = os.path.join(root, file)

                loader = PyPDFLoader(path)

                documents.extend(loader.load())

    return documents