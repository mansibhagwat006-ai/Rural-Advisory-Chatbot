from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

emb = HuggingFaceEmbeddings(
    model_name ="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

db = FAISS.load_local("vectorstore",emb, allow_dangerous_deserialization=True)

query ="what is the loan limit for shishu loan?"
for d in db.similarity_search(query, k = 3):
    print(d.metadata["source"], "page", d.metadata["page"])
    print(d.page_content[:300])
    print("-"*50)
