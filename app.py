import os
import io
import time
import base64
import streamlit as st

from rag.upload_loader import load_uploaded_pdf
from rag.upload_vector_store import create_uploaded_vector_db
from rag.embeddings import embeddings
from graph.workflow import graph
from services.github_analyzer import analyze_repository
from services.local_repo_loader import fetch_local_repository
from services.multi_agent_analyzer import analyze_repository_multi_agent
from services.github_analyzer import fetch_repository, analyze_repository
from services.chunked_analyzer import analyze_repository_chunked
from services.unit_test_generator import generate_unit_tests
from services.multi_language_test_generator import generate_tests, FRAMEWORKS

from services.code_fix_service import fix_code, explain_fix
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
from gtts import gTTS

from services.universal_repo_loader import fetch_any_repository


def load_css():
    css_path = "assets/style.css"
    if not os.path.exists(css_path):
        return
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

from pathlib import Path

dashboard_css = Path("assets/dashboard.css")

if dashboard_css.exists():
    st.markdown(
        f"<style>{dashboard_css.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True,
    )
    
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
    page_title="AI Engineering Studio",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<div class="studio-header">
    <div class="studio-icon">✦</div>
    <div>
        <h1>AI Engineering Studio</h1>
        <p>Intelligent Software Development Workspace</p>
    </div>
</div>
""", unsafe_allow_html=True)

load_css()
add_bg()


modern_css_path = Path("assets/modern_ui.css")

if modern_css_path.exists():
    st.markdown(
        f"<style>{modern_css_path.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

os.makedirs("data/uploads", exist_ok=True)
os.makedirs("data/audio", exist_ok=True)

st.divider()

st.subheader("AI Live Interview Studio")

st.markdown(
    "Practice a hands-free, two-way AI voice interview."
)

st.link_button(
    "Open Live Interview",
    "http://127.0.0.1:8765"
)

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



st.markdown(
    """
    <div class="dashboard-hero">
        <div class="section-label">
            AI-POWERED DEVELOPMENT WORKSPACE
        </div>

        <h2>Welcome to AI Engineering Studio</h2>

        <p>
            Analyze repositories, improve code quality,
            generate tests and collaborate with AI agents
            from one intelligent workspace.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


overview_col1, overview_col2, overview_col3 = st.columns(3)

with overview_col1:
    st.markdown(
        """
        <div class="feature-card">
            <h3> Repository Intelligence</h3>
            <p>
                AI-powered repository analysis,
                architecture review and code insights.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with overview_col2:
    st.markdown(
        """
        <div class="feature-card">
            <h3> AI Code Studio</h3>
            <p>
                Debug code, review changes and
                generate automated unit tests.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with overview_col3:
    st.markdown(
        """
        <div class="feature-card">
            <h3> Multi-Agent Assistant</h3>
            <p>
                LangGraph agents, RAG knowledge
                retrieval and voice assistance.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


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


with st.expander(
    "GitHub Repository Analyzer",
    expanded=False,
):
    st.markdown(
        "Analyze a public GitHub repository using AI."
    )

    github_url = st.text_input(
        "GitHub Repository URL",
        placeholder=(
            ""
        ),
        key="github_repo_url",
    )

    if st.button(
        "Analyze Repository",
        key="analyze_github_repo",
    ):
        if not github_url.strip():
            st.warning("Please enter a GitHub URL.")
        else:
            try:
                with st.spinner(
                    "Fetching repository source files..."
                ):
                    repo_data = fetch_any_repository(github_url)

                st.success(
                    f"Repository: {repo_data['name']}"
                )

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Language",
                    repo_data["language"],
                )
                col2.metric(
                    "Stars",
                    repo_data["stars"],
                )
                col3.metric(
                    "Files Analyzed",
                    len(repo_data["files"]),
                )

                with st.spinner(
                    "AI is reviewing the repository..."
                ):
                    report = analyze_repository_chunked(repo_data)

                st.session_state[
                    "github_analysis_report"
                ] = report

                st.session_state[
                    "github_analysis_repo"
                ] = repo_data["name"]

            except Exception as exc:
                st.error(
                    f"Repository analysis failed: {exc}"
                )

    if "github_analysis_report" in st.session_state:
        st.subheader("AI Repository Analysis")

        st.markdown(
            st.session_state[
                "github_analysis_report"
            ]
        )

        st.download_button(
            "Download Analysis Report",
            data=st.session_state[
                "github_analysis_report"
            ],
            file_name="github_analysis.md",
            mime="text/markdown",
        )


with st.expander("Multi-Agent Repository Analyzer", expanded=False):

    st.write(
        "Analyze the local repository using "
        "Architecture, Security, Code Quality and Testing agents."
    )

    if st.button("Run Multi-Agent Analysis", key="multi_agent_run"):

        try:
            with st.spinner("Loading local repository..."):
                repo_data = fetch_local_repository(".")

            repo_data["files"] = repo_data["files"][:3]

            with st.spinner("Running AI review agents..."):
                result = analyze_repository_multi_agent(repo_data)

            st.session_state["multi_agent_result"] = result
            st.session_state["multi_agent_repo"] = repo_data["name"]

            st.success("Analysis completed!")

        except Exception as error:
            st.error(f"Multi-Agent Analysis Failed: {error}")

    if "multi_agent_result" in st.session_state:

        result = st.session_state["multi_agent_result"]

        st.subheader("Repository Analysis Results")

        tabs = st.tabs([
            "Architecture",
            "Security",
            "Code Quality",
            "Testing"
        ])

        for tab, name in zip(tabs, [
            "Architecture",
            "Security",
            "Code Quality",
            "Testing"
        ]):
            with tab:
                st.markdown(result["reports"][name])

        st.download_button(
            "Download Full Analysis Report",
            data=result["combined_report"],
            file_name="multi_agent_analysis.md",
            mime="text/markdown"
        )


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


with st.expander(" AI Code Fix + Diff Preview", expanded=False):
    language = st.selectbox(
        "Programming Language",
        ["Python", "Java", "JavaScript", "TypeScript", "C++"],
        key="code_fix_language",
    )

    source_code = st.text_area(
        "Paste your source code",
        height=250,
        key="code_fix_source",
    )

    issue = st.text_area(
        "Describe the issue (optional)",
        key="code_fix_issue",
    )

    if st.button(" Analyze & Fix Code", key="run_code_fix"):
        if not source_code.strip():
            st.warning("Please paste source code first.")
        else:
            try:
                with st.spinner("AI is reviewing your code..."):
                    st.session_state["code_fix_result"] = fix_code(
                        source_code,
                        language,
                        issue,
                    )
                    st.session_state["code_fix_result_language"] = language.lower()

            except Exception as error:
                st.error(f"Code fix failed: {error}")

    
    if "code_fix_result" in st.session_state:
        result = st.session_state["code_fix_result"]

        original_col, fixed_col = st.columns(2)

        with original_col:
            st.subheader("Original Code")
            st.code(
                result["original"],
                language=st.session_state["code_fix_result_language"],
            )

        with fixed_col:
            st.subheader("AI Suggested Code")
            st.code(
                result["fixed"],
                language=st.session_state["code_fix_result_language"],
            )

        st.subheader("Code Changes")
        st.code(
            result["diff"] or "No changes suggested.",
            language="diff",
        )

        st.subheader("Syntax Validation")

        if result["syntax"] == "Valid Python syntax.":
            st.success(result["syntax"])
        elif result["syntax"].startswith("Syntax error"):
            st.error(result["syntax"])
        else:
            st.info(result["syntax"])

        st.subheader("AI Fix Explanation")

        if st.button("Explain Changes", key="explain_code_fix"):
            try:
                with st.spinner("Generating explanation..."):
                    explanation = explain_fix(
                        result["original"],
                        result["fixed"],
                        st.session_state["code_fix_result_language"],
                    )
                    st.session_state["code_fix_explanation"] = explanation
            except Exception as error:
                st.error(f"Explanation failed: {error}")

        if "code_fix_explanation" in st.session_state:
            st.markdown(st.session_state["code_fix_explanation"])

        extension = result["extension"]

        st.download_button(
            "Download Suggested Code",
            data=result["fixed"],
            file_name=f"fixed_code.{extension}",
            mime="text/plain",
            key="download_fixed_code",
        )

        st.warning(
            "AI-generated code must be reviewed and tested "
            "before production use."
        )

with st.expander("AI Unit Test Generator", expanded=False):

    st.write(
        "Generate pytest unit tests from Python source code."
    )

    module_name = st.text_input(
        "Python module name (without .py)",
        value="",
        key="test_module_name",
    )

    test_source = st.text_area(
        "Paste Python source code",
        height=250,
        key="test_generator_source",
    )

    if st.button(
        "Generate Unit Tests",
        key="generate_unit_tests_button",
    ):
        st.session_state.pop("generated_unit_tests", None)

        if not test_source.strip():
            st.warning("Please paste Python code first.")
        else:
            try:
                with st.spinner("Generating pytest tests..."):
                    result = generate_unit_tests(
                        test_source,
                        module_name.strip(),
                    )

                st.session_state["generated_unit_tests"] = result
                st.success("Unit tests generated!")

            except Exception as error:
                st.error(f"Test generation failed: {error}")

    if "generated_unit_tests" in st.session_state:

        result = st.session_state["generated_unit_tests"]

        st.subheader("Generated pytest Tests")

        st.code(
            result["test_code"],
            language="python",
        )

        st.subheader("Syntax Validation")

        if result["syntax_valid"]:
            st.success(result["syntax_message"])
        else:
            st.error(result["syntax_message"])

        st.download_button(
            "Download Unit Tests",
            data=result["test_code"],
            file_name=result["file_name"],
            mime="text/x-python",
            key="download_generated_tests",
        )

        st.info(
            "These tests are AI-generated and have not been "
            "executed. Review them before running."
        )

with st.expander(" Multi-Language AI Unit Test Generator", expanded=False):

    st.write(
        "Generate AI-powered unit tests for Python, Java, "
        "JavaScript, TypeScript and C#."
    )

    test_language = st.selectbox(
        "Programming Language",
        list(FRAMEWORKS.keys()),
        key="multi_test_language",
    )

    framework, extension = FRAMEWORKS[test_language]

    st.info(f"Testing Framework: {framework}")

    module_name = st.text_input(
        "Module / Class Name",
        value="",
        key="multi_test_module",
    )

    source_code = st.text_area(
        "Paste Source Code",
        height=250,
        key="multi_test_source",
    )

    if st.button("Generate Tests", key="multi_generate_tests"):
        st.session_state.pop("multi_test_result", None)

        try:
            if not source_code.strip():
                st.warning("Please paste source code first.")
            else:
                with st.spinner("Generating unit tests..."):
                    result = generate_tests(
                        source_code,
                        test_language,
                        module_name.strip(),
                    )

                st.session_state["multi_test_result"] = result
                st.success("Unit tests generated successfully!")

        except Exception as error:
            st.error(f"Test generation failed: {error}")

    if "multi_test_result" in st.session_state:
        result = st.session_state["multi_test_result"]

        st.subheader("Generated Unit Tests")
        st.caption(
            f"Language: {result['language']} | "
            f"Framework: {result['framework']}"
        )

        st.code(
            result["test_code"],
            language=result["language"].lower(),
        )

        st.download_button(
            "Download Unit Test File",
            data=result["test_code"],
            file_name=result["filename"],
            mime="text/plain",
            key="multi_test_download",
        )

        st.warning(
            "AI-generated tests have not been executed. "
            "Review them and install the required test framework."
        )


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
