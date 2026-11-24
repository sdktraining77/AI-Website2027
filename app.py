
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
    font-size: 34px;
    font-weight: 800;
    color: #C4B5FD;
    margin-bottom: 5px;
}

.subtitle {
    color: #94A3B8;
    font-size: 15px;
}

.welcome-container {
    background: linear-gradient(135deg, #151F35, #1C2340);
    border: 1px solid #37446A;
    border-radius: 18px;
    padding: 35px;
    text-align: center;
    margin-top: 35px;
    margin-bottom: 25px;
}

.welcome-icon {
    font-size: 42px;
    margin-bottom: 10px;
}

.welcome-title {
    font-size: 25px;
    font-weight: 700;
    color: #E2E8F0;
}

.welcome-text {
    color: #94A3B8;
    font-size: 15px;
    margin-top: 10px;
}

.source-card {
    background: #11182B;
    border-left: 4px solid #8B5CF6;
    padding: 12px;
    border-radius: 8px;
    margin: 8px 0;
}

[data-testid="stChatMessage"] {
    background-color: #11182B;
    border: 1px solid #283653;
    border-radius: 14px;
    padding: 15px;
}

[data-testid="stChatInput"] {
    border-color: #8B5CF6;
}

.stButton button {
    border-radius: 10px;
    border: 1px solid #37446A;
}

</style>
""", unsafe_allow_html=True)


# =========================
# Session State
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================
# Sidebar
# =========================
with st.sidebar:

    st.markdown("## 🤖 Training Center AI")

    st.caption("Your intelligent training assistant")

    st.divider()

    st.markdown("### ⚙️ System Information")

    st.write("**Embedding Model**")
    st.caption("BAAI/bge-small-en-v1.5")

    st.write("**Language Model**")
    st.caption("openai/gpt-oss-120b")

    st.write("**Retrieval Configuration**")
    st.caption("Top K: 3")
    st.caption("Similarity Threshold: 0.6")

    st.divider()

    st.markdown("### 📚 Knowledge Base")
    st.caption("6 training center documents")

    st.divider()

    if st.button("🗑️ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

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
    '<div class="subtitle">'
    'Get accurate answers about training courses and center services.'
    '</div>',
    unsafe_allow_html=True
)

st.write("")


# =========================
# Welcome Screen
# =========================
if not st.session_state.messages:

    st.markdown("""
    <div class="welcome-container">
        <div class="welcome-icon">🤖</div>
        <div class="welcome-title">How can I help you today?</div>
        <div class="welcome-text">
            Ask me about training courses, registration, schedules,
            and everything related to the training center.
        </div>
    </div>
    """, unsafe_allow_html=True)


# =========================
# Chat History
# =========================
st.markdown("### 💬 Conversation")

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if (
            message["role"] == "assistant"
            and message.get("supported", False)
            and message.get("sources")
        ):

            with st.expander("📂 View Sources"):

                for source in message["sources"]:

                    st.markdown(
                        f"""
                        <div class="source-card">
                            <b>📄 {source}</b>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )


# =========================
# Chat Input
# =========================
question = st.chat_input(
    "Ask something about the training center..."
)

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
                supported = result["supported"]

                st.markdown(answer)

                if supported and sources:

                    with st.expander("📂 View Sources"):

                        displayed_files = set()

                        for source in sources:

                            if source not in displayed_files:

                                st.markdown(
                                    f"""
                                    <div class="source-card">
                                        <b>📄 {source}</b>
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )

                                displayed_files.add(source)

                else:
                    st.info("No supporting sources were found.")

                # Save assistant response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources if supported else [],
                    "supported": supported
                })

            except Exception as e:

                st.error(f"An error occurred: {e}")
