import streamlit as st
from chatbot import ask_ai
from file_handler import read_file
from rag import create_vector_store, get_relevant_context
import time

st.set_page_config(page_title="ClaudeIQ", layout="wide")

# 🎨 Custom CSS (Header + Robot GIF)
st.markdown("""
<style>
.header {
    position: sticky;
    top: 0;
    background-color: #0f172a;
    padding: 15px;
    z-index: 999;
    border-bottom: 1px solid #333;
}

.header-container {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 15px;
}

.title {
    font-size: 45px;
    color: #38bdf8;
    margin: 0;
}

.subtitle {
    text-align: center;
    color: gray;
    margin-top: 5px;
}

.creator {
    text-align: center;
    font-size: 14px;
    color: #888;
}

.robot {
    width: 60px;
    border-radius: 50%;
}
</style>
""", unsafe_allow_html=True)

# 🎯 Header
st.markdown("""
<div class="header">
    <div class="header-container">
        <img class="robot" src="https://media.giphy.com/media/l41lFw057lAJQMwg0/giphy.gif">
        <div class="title">ClaudeIQ</div>
    </div>
    <div class="subtitle">Smart AI Chatbot with Memory & RAG</div>
    <div class="creator">Created by <b>Lalit Singh</b> 🚀</div>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

# 📂 File upload (UPDATED TEXT)
uploaded_files = st.file_uploader(
    "📂 Upload a file for analysis", 
    accept_multiple_files=True
)

# 🔍 Build vector DB
if uploaded_files:
    all_text = ""

    with st.spinner("📚 Indexing files..."):
        for file in uploaded_files:
            content = read_file(file)

            if hasattr(content, "to_string"):
                all_text += content.to_string()
            else:
                all_text += str(content)

        st.session_state.vector_store = create_vector_store(all_text)

    st.success("Files indexed with RAG ✅")

# 💬 Chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 💬 User input (UPDATED TEXT)
if prompt := st.chat_input("💬 Message to ask something..."):

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    context = ""
    if st.session_state.vector_store:
        context = get_relevant_context(
            st.session_state.vector_store, prompt
        )

    with st.chat_message("assistant"):
        with st.spinner("🤖 ClaudeIQ is thinking..."):
            response = ask_ai(prompt, context, st.session_state.messages)

        message_placeholder = st.empty()
        full_response = ""

        for char in response:
            full_response += char
            message_placeholder.markdown(full_response)
            time.sleep(0.01)

    st.session_state.messages.append({"role": "assistant", "content": response})