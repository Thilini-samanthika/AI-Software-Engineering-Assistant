import os

documents=[]

folder="data/pdfs"

for file in os.listdir(folder):

    if file.endswith(".pdf"):

        path=os.path.join(folder,file)

        documents.extend(load_documents(path))