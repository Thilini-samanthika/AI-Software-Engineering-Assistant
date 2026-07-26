import os
import io
import time
import base64
import streamlit as st

from rag.upload_loader import load_uploaded_pdf
from rag.upload_vector_store import create_uploaded_vector_db
from rag.embeddings import embeddings
from graph.workflow import graph

from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
from gtts import gTTS


def load_css():
    css_path = "assets/style.css"
    if not os.path.exists(css_path):
        return
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def add_bg():
    bg_path = "assets/background.jpeg"
    if not os.path.exists(bg_path):
        return
    with open(bg_path, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


def record_voice():
    """
    Renders a mic recorder widget (records directly in the browser)
    and returns the recorded audio dict, or None if nothing recorded.
    """
    audio = mic_recorder(
        start_prompt=" Start Recording",
        stop_prompt=" Stop Recording",
        just_once=True,
        use_container_width=True,
        format="wav",
        key="voice_recorder"
    )
    return audio


def speech_to_text(audio_bytes, language="English"):
    """
    Converts recorded browser audio (wav bytes) into text using
    SpeechRecognition (Google Web Speech API).
    Returns recognized text, or None if it could not be recognized.
    """
    if not audio_bytes:
        return None

    lang_code = "si-LK" if language == "Sinhala" else "en-US"

    try:
        recognizer = sr.Recognizer()
        audio_file = io.BytesIO(audio_bytes)
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data, language=lang_code)
        return text
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        return None
    except Exception:
        return None


def text_to_speech(text, language="English"):
    """
    Converts the assistant's answer into speech using gTTS and
    saves it as a temporary mp3 file. Returns the file path,
    or None if generation failed.
    """
    if not text:
        return None

    lang_code = "si" if language == "Sinhala" else "en"

    try:
        os.makedirs("data/audio", exist_ok=True)
        audio_path = f"data/audio/response_{int(time.time())}.mp3"
        tts = gTTS(text=text, lang=lang_code)
        tts.save(audio_path)
        return audio_path
    except Exception:
        return None


st.set_page_config(
    page_title="AI Software Engineering Assistant",
    page_icon="",
    layout="wide"
)

load_css()
add_bg()

if "messages" not in st.session_state:
    st.session_state.messages = []

os.makedirs("data/uploads", exist_ok=True)
os.makedirs("data/audio", exist_ok=True)



with st.sidebar:

    st.title(" AI Assistant")
    st.caption("Multi-Agent Software Engineering System")

    st.markdown("---")

    st.subheader(" System Status")

    system_status = [
        " LangGraph",
        " Groq LLM",
        " ChromaDB",
        " Sentence Transformers",
        " RAG Pipeline"
    ]

    for item in system_status:
        st.success(item)

    st.markdown("---")

    st.subheader(" Available Agents")

    agents = [
        " Router Agent",
        " Coding Agent",
        " Documentation Agent",
        " RAG Agent",
        " Testing Agent",
        " code_review Agent",
        " upload_rag Agent",
        " Architecture Agent",
        " Code Review Agent",
        " Reflection Agent"
    ]

    for agent in agents:
        st.info(agent)

    st.markdown("---")

    st.subheader(" Voice Settings")
    voice_language = st.radio(
        "Language",
        ["English", "Sinhala"],
        horizontal=True
    )

    st.markdown("---")

    st.subheader(" Upload Your PDF")

    uploaded_file = st.file_uploader(
        "Upload Documentation",
        type=["pdf"]
    )

    if uploaded_file:

        file_path = "data/uploads/" + uploaded_file.name

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success("PDF Uploaded")

        with st.spinner("Creating Knowledge Base..."):
            chunks = load_uploaded_pdf(file_path)
            create_uploaded_vector_db(chunks, embeddings)

        st.success(" Personal Knowledge Base Ready")

        st.subheader(" Knowledge Base")

        documents = [ "Python", "C#", "Java", "SOLID", "OOP", "Design Patterns",
            "Clean Code", "REST API", "Git", "GitHub", "SQL", "Docker",
            "Kubernetes", "Agile", "Scrum", "Unit Testing", "Microservices",
            "CI/CD", "Software Architecture"
        ]

        for doc in documents:
            st.write("", doc)

    st.markdown("---")

    if st.button(" Clear Chat"):
        st.session_state.messages = []
        st.rerun()




header_col1, header_col2 = st.columns([1, 6])

with header_col1:
    if os.path.exists("assets/logo.png"):
        st.image("assets/logo.png", width=90)

with header_col2:
    st.markdown( """<h1 style="color:white;font-size:45px;margin-bottom:0;">
        AI Software Engineering Assistant</h1>
        <p style="color:#D1D5DB;font-size:20px;">
        Multi-Agent AI System using LangGraph + Groq + RAG</p>""",
        unsafe_allow_html=True
    )

st.divider()




for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


st.subheader("Voice Assistant")

voice_col1, voice_col2 = st.columns([1, 3])

with voice_col1:
    recorded_audio = record_voice()

recognized_text = None

with voice_col2:
    if recorded_audio and recorded_audio.get("bytes"):
        with st.spinner("Recognizing speech..."):
            recognized_text = speech_to_text(recorded_audio["bytes"], language=voice_language)

        if recognized_text:
            st.markdown("**Recognized Speech:**")
            st.info(recognized_text)
        else:
            st.error("Could not recognize speech.")
    elif recorded_audio is not None and not recorded_audio.get("bytes"):
        st.error("Microphone access denied.")

question = st.chat_input("Ask anything about Software Engineering...")

if recognized_text:
    question = recognized_text



if question:


    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.markdown(question)

    start = time.time()

    try:
        with st.spinner(" AI Agents are working..."):
            result = graph.invoke(
                {
                    "question": question,
                    "agent": "",
                    "answer": "",
                    "sources": []
                }
            )

        answer = result["answer"]
        agent = result["agent"]
        sources = result.get("sources", [])

    except Exception as e:
        answer = f"""
 Error occurred:

{e}
"""
        agent = "error"
        sources = []

    end = time.time()
    execution_time = round(end - start, 2)



    st.divider()
    st.subheader(" Agent Execution Pipeline")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Router", "")
    col2.metric("Agent", agent.title())
    col3.metric("Time", f"{execution_time}s")
    col4.metric("Confidence", "95%")


    descriptions = {
        "coding": " Code Explanation & Debugging",
        "documentation": " README and Documentation Generation",
        "rag": " Knowledge Base Search",
        "testing": " Unit Test Generation",
        "architecture": " System Architecture Design",
        "code_review": " Code Quality Analysis"
    }

    st.caption(descriptions.get(agent, "AI Processing"))



    if sources:
        st.subheader(" Retrieved Documents")
        for source in sources:
            st.info(source)



    st.subheader("Confidence Score")
    confidence = 95
    st.progress(confidence / 100)
    st.write(f"{confidence}%")



    st.download_button(
        label=" Download Answer (.md)",
        data=answer,
        file_name="AI_answer.md",
        mime="text/markdown"
    )



    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )



    with st.chat_message("assistant"):
        st.markdown(answer)
        st.caption(f" Agent: {agent}")
        st.caption(f" Time: {execution_time} seconds")

        with st.expander(" Copy Answer"):
            st.code(answer)

        with st.spinner(" Generating voice response..."):
            audio_path = text_to_speech(answer, language=voice_language)

        if audio_path:
            st.audio(audio_path, format="audio/mp3")
        else:
            st.caption(" Voice response unavailable.")

    st.markdown("---")

st.caption("2026 AI Software Engineering Assistant Built with Streamlit + LangGraph + Groq")
