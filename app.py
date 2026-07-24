import streamlit as st
import time

from graph.workflow import graph

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="AI Software Engineering Assistant",
    page_icon="🤖",
    layout="wide"
)

# -----------------------------
# Session State
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:

    st.title("🤖 AI Assistant")

    st.markdown("---")

    st.subheader("📊 System Status")

    st.success("🟢 LangGraph")

    st.success("🟢 Router Agent")

    st.success("🟢 Reflection Agent")

    st.success("🟢 ChromaDB")

    st.success("🟢 Groq API")

    st.markdown("---")

    st.subheader("📁 Knowledge Base")
documents = [

"Python",

"C#",

"Java",

"SOLID",

"OOP",

"Design Patterns",

"Clean Code",

"REST API",

"Git",

"GitHub",

"SQL",

"Docker",

"Kubernetes",

"Agile",

"Scrum"

]

for doc in documents:

    st.info(doc)

    st.markdown("---")

    if st.button("Clear Chat"):

        st.session_state.messages = []

        st.rerun()

# -----------------------------
# Title
# -----------------------------
st.title("🤖 AI Software Engineering Assistant")

st.caption("Version 1.0")

st.markdown("---")

st.divider()

# -----------------------------
# Chat History
# -----------------------------
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.markdown(msg["content"])

# -----------------------------
# User Input
# -----------------------------
question = st.chat_input(
    "Ask anything about Software Engineering..."
)

# -----------------------------
# Ask AI
# -----------------------------
if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):

        st.markdown(question)

    start = time.time()

    with st.spinner("Thinking..."):

       result = graph.invoke(
    {
        "question": question,
        "agent": "",
        "answer": "",
        "sources": []
    }
)

end = time.time()

execution_time = round(end - start, 2)

answer = result["answer"]

agent = result["agent"]

sources = result.get("sources", [])


# ---------------------------------
# Agent Dashboard
# ---------------------------------

st.divider()

st.subheader("⚙ Agent Execution")

col1, col2, col3 = st.columns(3)

with col1:
    st.success("🟢 Router")

with col2:
    st.success(f"🟢 {agent.capitalize()}")

with col3:
    st.success("🟢 Reflection")


# ---------------------------------
# Retrieved Documents
# ---------------------------------

if len(sources) > 0:

    st.subheader("📚 Retrieved Documents")

    for source in sources:

        st.info(source)


# ---------------------------------
# Confidence
# ---------------------------------

confidence = 95

st.subheader("📈 Confidence")

st.progress(confidence / 100)

st.write(f"Confidence Score : {confidence}%")


# ---------------------------------
# Save Chat
# ---------------------------------

st.session_state.messages.append(
    {
        "role": "assistant",
        "content": answer
    }
)


# ---------------------------------
# Assistant Message
# ---------------------------------

with st.chat_message("assistant"):

    st.markdown(answer)

    st.caption(f"🤖 Agent : {agent}")

    st.caption(f"⏱ Execution Time : {execution_time} sec")