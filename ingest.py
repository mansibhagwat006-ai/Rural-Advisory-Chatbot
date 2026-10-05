import glob
import os 
import numpy as np
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

docs = []
for path in glob.glob("data/*.pdf"):
    page = PyPDFLoader(path).load()
    for p in page:
        p.metadata["source"] = os.path.basename(path)
    docs.extend(page)
    print(f"Loaded {len(page)} pages from {path}")

docs = [d for d in docs if len(d.page_content.strip())>20]
print(f"Total usable pages: {len(docs)}")

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 800 , chunk_overlap = 100
)
chunks = splitter.split_documents(docs)
print(f"Total chunks: {len(chunks)}")

embeddings = HuggingFaceEmbeddings(
    model = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

db = FAISS.from_documents(chunks , embeddings)
db.save_local("vectorstore")
print("Vector store saved!")