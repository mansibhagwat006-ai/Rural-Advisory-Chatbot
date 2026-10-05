import streamlit as st
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent 
from tools import calculate_emi , monthly_profit , break_even , loan_affordability

SYSTEM_PROMPT = """You are a friendly business advisor for rural micro-entrepreneurs in India.

Rules:
1. Use simple, short sentences. Reply in the same language the user writes in (Hindi, Gujarati, English, etc.).
2. For ANY question about scheme rules, eligibility, loan limits, interest, or documents, ALWAYS call search_schemes first. Never answer these from memory.
3. Cite sources as (filename, page) after each fact you take from the documents.
4. For ANY calculation, use the calculator tools. Never calculate yourself.
5. If the documents do not contain the answer, say so honestly and advise the user to contact the nearest bank branch or District Industries Centre (DIC).
6. If the user's business details are missing, ask one short question to get them.
7. You give guidance, not guaranteed loan approval."""

@st.cache_resource
def load_agent():
    embeddings = HuggingFaceEmbeddings(
        model_name ="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    ) 

    db = FAISS.load_local(
        "vectorstore", embeddings , allow_dangerous_deserialization=True
    )

    @tool
    def search_schemes(query:str)->str:
        """Search MUDRA, MSME and NABARD documents for scheme rules,
        eligibility, loan limits, interest rates and required documents."""
        results = db.similarity_search(query , k = 4)
        return "\n\n".join(
            f"[{d.metadata['source']}, page {d.metadata.get('page',0)+1}]\n{d.page_content}"
            for d in results
        ) 

    llm = ChatGroq(
        model = "openai/gpt-oss-120b",
        api_key = st.secrets["GROQ_API_KEY"],
        temperature = 0 
    )

    tools = [search_schemes,calculate_emi, monthly_profit,break_even,loan_affordability]
    return create_react_agent(llm , tools ,prompt=SYSTEM_PROMPT)