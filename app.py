import streamlit as st
from rag import load_agent

def extract_text(content):
    """Turn LLM output (string or list of blocks) into plain text."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(block["text"])
            elif isinstance(block, str):
                parts.append(block)
        return "\n".join(parts)
    return str(content)

st.set_page_config(page_title = "RURAL BUSINESS ADVISOR", page_icon = "🌾", layout = "centered")
st.title("🌾 Rural Business Advisor")
st.caption("Ask about MUDRA, MSME and NABARD schemes, or calculate your loan and profit.")

with st.sidebar:
    st.header("Your business")
    biz = st.selectbox("Business type", ["Kirana shop", "Dairy", "Tailoring", "Food processing", "Farming", "Other"])
    loc = st.text_input("Village / District")
    income = st.number_input("Monthly income (₹)", min_value=0, step=1000)
    language = st.selectbox("Reply language", ["Same as my question", "Hindi", "Gujarati", "English"])
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()

agent = load_agent()

# ---------- Chat history ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# ---------- Chat input ----------
if question := st.chat_input("Ask about loans, schemes, or your profit..."):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    profile = (
        f"[User profile: business={biz}, location={loc or 'unknown'}, "
        f"monthly income=₹{income}, reply language={language}]\n"
    )
    history = [(m["role"], m["content"]) for m in st.session_state.messages[:-1]]

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                out = agent.invoke({"messages": history + [("user", profile + question)]})
                answer = extract_text(out["messages"][-1].content)
            except Exception as e:
                answer = "Sorry, something went wrong. Please try again."
                st.error(str(e))
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

st.divider()
st.caption("⚠️ This is guidance only. Please confirm details with your bank or District Industries Centre.")