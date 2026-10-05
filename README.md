# 🌾 Rural Business Advisor

An AI chatbot that helps rural micro-entrepreneurs understand MUDRA, MSME and NABARD loan schemes, and calculate EMI, profit and affordability. 

**Live demo:https://rural-advisory-chatbot-eptbkrxnvy38acdhnnmct8.streamlit.app/** 

## Problem
Loan rules sit inside long, formal government PDFs. Many small business owners can't easily find which scheme fits them, what documents they need, or whether they can afford the repayments.

## Solution
A chat advisor that:
- Answers scheme questions in simple language, grounded in official documents (RAG)
- Cites the source file and page for each fact
- Uses calculator tools for EMI, monthly profit, break-even and loan affordability
- Personalises advice using the user's business type, location and income
- Falls back to "contact your nearest bank or DIC" when the documents don't have the answer

## How it works
```
User question → LLM agent → Document search (FAISS) or Calculator tools → Cited answer
```

## Tech stack
- **UI and hosting:** Streamlit
- **Orchestration:** LangChain, LangGraph
- **LLM:** Groq ([model name])
- **Embeddings:** sentence-transformers (paraphrase-multilingual-MiniLM-L12-v2)
- **Vector DB:** FAISS
- **PDF loading and chunking:** PyPDFLoader, RecursiveCharacterTextSplitter (800 chars, 100 overlap)

## Project structure
```
├── app.py            # Streamlit chat UI
├── rag.py            # Agent, retriever and prompt
├── tools.py          # EMI, profit, break-even, affordability tools
├── ingest.py         # Builds the vector store from PDFs
├── test_retrieval.py # Checks retrieval quality
├── data/             # Source PDFs
├── vectorstore/      # Saved FAISS index
└── requirements.txt
```

## Run locally
```bash
git clone https://github.com/mansibhagwat006-ai/Rural-Advisory-Chatbot.git
cd rural-advisor
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```
Create `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "your-key"
```
Build the index (only needed if you change the PDFs), then run:
```bash
python ingest.py
streamlit run app.py
```

## Limitations
- Answers depend on the PDFs provided and may be out of date. Verify with your bank or District Industries Centre.
- This is guidance only, not a loan approval.

## Future work
Voice input, regional-language support, WhatsApp channel, low-bandwidth mode.

## Author
MANSI BHAGWAT  - mansibhagwat006@gmail.com
