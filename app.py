
import streamlit as st
from src.retrieval.rag_chatbot import ask_question

# =========================
# Page Configuration
# =========================
st.set_page_config(
    page_title="Training Center AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# =========================
# Custom CSS
# =========================
st.markdown("""
<style>
.stApp {
    background-color: #0B1020;
    color: #F1F5F9;
}

[data-testid="stSidebar"] {
    background-color: #11182B;
}

.main-title {
    font-size: 36px;
    font-weight: 800;
    color: #A78BFA;
}

.subtitle {
    color: #94A3B8;
    font-size: 16px;
}

.metric-card {
    background: #151F35;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #283653;
    text-align: center;
}

.metric-value {
    color: #A78BFA;
    font-size: 28px;
    font-weight: bold;
}

.metric-label {
    color: #94A3B8;
    font-size: 14px;
}

.answer-card {
    background: #151F35;
    border: 1px solid #37446A;
    padding: 22px;
    border-radius: 14px;
    margin-top: 15px;
}

.source-card {
    background: #11182B;
    border-left: 4px solid #8B5CF6;
    padding: 12px;
    border-radius: 8px;
    margin: 8px 0;
}
</style>
""", unsafe_allow_html=True)

# =========================
# Session State
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_sources" not in st.session_state:
    st.session_state.last_sources = []

# =========================
# Sidebar
# =========================
with st.sidebar:
    st.markdown("## 🤖 AI Assistant")
    st.caption("Training Center RAG Chatbot")

    st.divider()

    st.markdown("### ⚙️ System Information")
    st.write("**Embedding Model**")
    st.caption("BAAI/bge-small-en-v1.5")

    st.write("**Language Model**")
    st.caption("openai/gpt-oss-20b")

    st.write("**Retrieval Settings**")
    st.caption("Top K: 3")
    st.caption("Similarity Threshold: 0.6")

    st.divider()

    if st.button("🗑️ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.last_sources = []
        st.rerun()

    st.markdown("### 📚 Knowledge Base")
    st.write("6 training center documents")

    st.divider()
    st.caption("Powered by LlamaIndex + Groq")

# =========================
# Main Header
# =========================
st.markdown(
    '<div class="main-title">Training Center AI Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Ask questions and get answers from the training center knowledge base.</div>',
    unsafe_allow_html=True
)

st.write("")

# =========================
# Dashboard Metrics
# =========================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">6</div>
        <div class="metric-label">Knowledge Documents</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">100%</div>
        <div class="metric-label">Retrieval Test Success</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">3</div>
        <div class="metric-label">Top K Results</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">0.6</div>
        <div class="metric-label">Similarity Threshold</div>
    </div>
    """, unsafe_allow_html=True)

st.caption(
    "Retrieval test success is based on the 10 recorded retrieval evaluation questions, "
    "not a guarantee of overall chatbot accuracy."
)

st.divider()

# =========================
# Chat History
# =========================
st.markdown("### 💬 Chat")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message["role"] == "assistant" and message.get("sources"):
            with st.expander("📂 View Sources"):
                for source in message["sources"]:
                    st.markdown(
                        f"""
                        <div class="source-card">
                            <b>📄 {source['file_name']}</b><br>
                            Similarity Score: {source['similarity_score']:.3f}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

# =========================
# Chat Input
# =========================
question = st.chat_input("Ask something about the training center...")

if question:
    # Display user question
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    # Generate answer
    with st.chat_message("assistant"):
        with st.spinner("Searching the knowledge base..."):
            try:
                result = ask_question(question)

                answer = result["answer"]
                sources = result["sources"]

                st.markdown(answer)

                if result["supported"] and sources:
                    with st.expander("📂 View Sources"):
                        # Display unique source files
                        displayed_files = set()

                        for source in sources:
                            file_name = source["file_name"]

                            if file_name not in displayed_files:
                                st.markdown(
                                    f"""
                                    <div class="source-card">
                                        <b>📄 {file_name}</b><br>
                                        Similarity Score:
                                        {source['similarity_score']:.3f}
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )
                                displayed_files.add(file_name)

                else:
                    st.info("No supporting sources were found.")

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })

            except Exception as e:
                st.error(f"An error occurred: {e}")
