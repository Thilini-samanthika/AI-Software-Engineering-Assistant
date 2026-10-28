
<div align="center">

#  AI Software Engineering Assistant

### A Multi-Agent AI System for Software Developers

**An AI-powered developer assistant for coding, debugging, documentation, software architecture, code review, testing, and intelligent knowledge retrieval.**

Built with **Python, LangGraph, LangChain, RAG, ChromaDB, Groq LLM, and Streamlit**.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-purple)
![LangChain](https://img.shields.io/badge/LangChain-AI_Framework-green)
![Streamlit](https://img.shields.io/badge/Streamlit-Web_App-red?logo=streamlit)
![Groq](https://img.shields.io/badge/Groq-LLM-orange)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_Database-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Interview_Studio-009688?logo=fastapi)

###  Live Application

[**Launch AI Software Engineering Assistant**](https://ai-software-engineering-assistant-ngsqmt5gnqkl3sa2psvwks.streamlit.app/)

[GitHub Repository](https://github.com/Thilini-samanthika/AI-Software-Engineering-Assistant)

</div>

---

##  Project Overview

**AI Software Engineering Assistant** is a multi-agent AI application developed to support software developers with common software engineering activities.

The application combines Large Language Models (LLMs), intelligent task routing, specialized AI agents, and Retrieval-Augmented Generation (RAG) to provide assistance with programming, debugging, documentation, architecture design, testing, and code review.

Instead of switching between multiple resources, developers can access AI-powered assistance through a single Streamlit application.

###  Project Objectives

- Support software developers with AI-assisted programming.
- Simplify code explanation and debugging.
- Generate software engineering documentation.
- Provide software architecture recommendations.
- Improve access to technical knowledge through RAG.
- Assist with unit testing and code reviews.
- Explore multi-agent workflows using LangGraph.
- Support technical interview preparation.

---

##  Key Features

###  1. AI Coding Assistant

- Explain source code.
- Answer programming questions.
- Identify potential programming errors.
- Suggest debugging solutions.
- Generate code examples.
- Recommend code improvements.

###  2. AI Documentation Generator

- Generate README documentation.
- Assist with API documentation.
- Explain technical concepts.
- Generate structured software documentation.

###  3. Retrieval-Augmented Generation (RAG)

- Search software engineering documentation.
- Retrieve relevant technical information.
- Upload PDF documents.
- Search uploaded knowledge sources.
- Generate responses using retrieved context.

###  4. Software Architecture Assistant

- Recommend software architectures.
- Explain architecture patterns.
- Suggest system components.
- Support high-level system design decisions.

###  5. AI Unit Test Generation

- Generate suggested unit tests.
- Identify common test scenarios.
- Suggest edge cases.
- Assist with testing across programming languages.

###  6. AI Code Review

- Review source code.
- Identify potential code quality issues.
- Suggest refactoring opportunities.
- Recommend maintainability improvements.

###  7. Multi-Agent AI System

The application uses specialized agents to handle different software engineering tasks.

Key components include:

- Router Agent
- Coding Agent
- Documentation Agent
- RAG Agent
- Testing Agent
- Architecture Agent
- Code Review Agent
- Reflection Agent

###  8. GitHub Repository Analysis

- Analyze repository structure.
- Explore source code organization.
- Assist with understanding unfamiliar codebases.
- Suggest potential improvements.

###  9. Voice Assistant

- Voice-based interaction.
- Speech recognition.
- Text-to-speech responses.
- Conversational AI assistance.

Voice functionality depends on microphone permissions and supported speech technologies.

###  10. AI Live Interview Studio

A separate browser-based interview practice environment.

**Interview Modes:**

- Mock Interview
- Guided Coaching
- HR Interview
- Technical Interview

**Technologies:**

- FastAPI
- WebSockets
- Browser Speech Recognition
- Speech Synthesis
- Groq LLM

The Interview Studio runs as a separate local service.

---

##  Multi-Agent Architecture

The application uses a router to direct requests toward specialized AI agents.

```text
                         USER
                           |
                           v
                    STREAMLIT UI
                           |
                           v
                     ROUTER AGENT
                           |
         +-----------------+-----------------+
         |                 |                 |
         v                 v                 v
    CODING AGENT    DOCUMENTATION AGENT   RAG AGENT
         |                 |                 |
         v                 v                 v
    TESTING AGENT   ARCHITECTURE AGENT   CHROMADB
         |
         v
    CODE REVIEW AGENT
         |
         v
    REFLECTION AGENT
         |
         v
     FINAL RESPONSE
```
---

##  Agent Responsibilities

| Agent | Responsibility |
|---|---|
| Router Agent | Selects an appropriate agent for the task |
| Coding Agent | Code explanation and debugging |
| Documentation Agent | README and API documentation generation |
| RAG Agent | Knowledge base retrieval |
| Testing Agent | Unit test generation |
| Architecture Agent | Software architecture recommendations |
| Code Review Agent | Code quality analysis |
| Reflection Agent | Response evaluation and improvement |

---

##  RAG Knowledge Base

The RAG system uses **ChromaDB** for vector-based knowledge retrieval.

The project's software engineering knowledge base covers topics such as:

| Category | Topics |
|---|---|
| Programming | Python, Java, C#, SQL |
| Software Design | SOLID Principles, OOP, Design Patterns |
| Code Quality | Clean Code, Refactoring |
| Backend Development | REST API, Microservices |
| Version Control | Git, GitHub |
| DevOps | Docker, Kubernetes, CI/CD |
| Project Management | Agile, Scrum |
| Architecture | Software Architecture |
| Testing | Unit Testing |

### RAG Processing Workflow

```text
PDF Documents
      |
      v
Document Loading
      |
      v
Text Splitting
      |
      v
Sentence Transformer Embeddings
      |
      v
ChromaDB Vector Storage
      |
      v
Relevant Document Retrieval
      |
      v
Groq LLM
      |
      v
Context-Aware Response
```

---

##  Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python 3.11 |
| Frontend | Streamlit |
| AI Workflow | LangGraph |
| LLM Framework | LangChain |
| LLM Provider | Groq |
| Vector Database | ChromaDB |
| Embeddings | Sentence Transformers |
| PDF Processing | PyPDFLoader |
| Interview Backend | FastAPI |
| Real-Time Communication | WebSockets |
| Voice Interaction | Speech Recognition, Text-to-Speech |
| Version Control | Git, GitHub |
| IDE | Visual Studio Code |

---

##  Project Structure

```text
AI-Software-Engineering-Assistant/
│
├── agents/
│   ├── router.py
│   ├── coding_agent.py
│   ├── documentation_agent.py
│   ├── rag_agent.py
│   ├── testing_agent.py
│   ├── architecture_agent.py
│   ├── code_review_agent.py
│   └── reflection_agent.py
│
├── graph/
│   └── workflow.py
│
├── llm/
│   ├── groq_client.py
│   └── openrouter_client.py
│
├── rag/
│   ├── loader.py
│   ├── splitter.py
│   ├── embeddings.py
│   ├── retriever.py
│   ├── vector_store.py
│   └── upload_loader.py
│
├── interview_studio/
│   ├── __init__.py
│   ├── index.html
│   └── server.py
│
├── services/
├── tests/
│
├── data/
│   ├── pdfs/
│   └── uploads/
│
├── assets/
│
├── app.py
├── config.py
├── requirements.txt
├── .gitignore
└── README.md
```

*The structure above summarizes the project's documented modules and recent additions. Refer to the repository for the exact current file tree.*

---

##  Installation Guide

### Prerequisites

- Python 3.11
- Git
- Visual Studio Code or another IDE
- Groq API key
- Internet connection

### Step 1 — Clone Repository

```bash
git clone https://github.com/Thilini-samanthika/AI-Software-Engineering-Assistant.git
```

```bash
cd AI-Software-Engineering-Assistant
```

### Step 2 — Create Virtual Environment

```bash
python -m venv .venv
```

Activate on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

For Linux/macOS:

```bash
source .venv/bin/activate
```

### Step 3 — Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 4 — Configure Environment Variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_groq_api_key_here
```

If your configuration uses OpenRouter, also set:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

**Never upload real API keys to GitHub.**

### Step 5 — Run Streamlit Application

```bash
python -m streamlit run app.py
```

Open:

http://localhost:8501

---

## 🎤Running the AI Live Interview Studio

The Live Interview Studio runs independently from the main Streamlit application.

Open another terminal and activate the virtual environment.

Run:

```bash
python -m uvicorn interview_studio.server:app --host 127.0.0.1 --port 8765
```

Open:

http://127.0.0.1:8765

### Interview Studio Requirements

- Supported web browser
- Microphone access
- Internet connection for AI responses
- Configured Groq API key
---

##  Application Screenshots

### Home Page

<img width="400" height="200" alt="image" src="https://github.com/user-attachments/assets/94adb173-5aa4-4b80-98af-570a8f435d83" />


### Chat Interface

<img width="400" height="200" alt="image" src="https://github.com/user-attachments/assets/dee72c91-dc7f-4859-9e20-b983712d80d5" />


### RAG Search

<img width="700" height="88" alt="image" src="https://github.com/user-attachments/assets/d21fb4f3-89e1-4b72-bac4-53459f7a7aa8" />


### PDF Upload

<img width="200" height="400" alt="PDF Knowledge Base Upload" src="https://github.com/user-attachments/assets/24beaca4-9c3e-47dd-b48b-748fbab037bd" />

---

##  Example Questions

### Programming

```text
Explain SOLID principles.

Review this Python code.

Debug this Java program.
```

### Documentation

```text
Generate a README for my project.

Generate API documentation.
```

### Testing

```text
Generate unit tests for this function.
```

### Architecture

```text
Design a Hospital Management System.

Explain the Repository Pattern.
```

### RAG

```text
Search Docker documentation.

Summarize the uploaded PDF.
```

### Interview Preparation

```text
Conduct a mock Software Engineering Internship interview.
```

---

## Security

- Store API keys in environment variables.
- Do not commit `.env` files.
- Keep uploaded documents and local vector databases private.
- Avoid hardcoding credentials.
- Review AI-generated code before execution.
- Validate generated tests.
- Do not upload confidential source code without permission.

---

##  Limitations

- AI-generated responses may contain errors.
- Cloud-based LLM features require internet access.
- API rate limits may apply.
- Generated code requires developer review.
- Browser speech recognition support varies.
- The Live Interview Studio requires a separate server.
- Some advanced AI workflows may require further testing and refinement.

---

##  Future Improvements

- AI Pair Programming
- Enhanced Multi-Agent Collaboration
- Improved GitHub Repository Analysis
- Multiple LLM Support
- Secure Code Execution Sandbox
- UML Diagram Generation
- Database Schema Generator
- Docker Deployment
- User Authentication
- CI/CD Automation

---

##  Developer

**M. Thilini Samanthika**

BSc (Hons) in Information Technology Undergraduate

**Areas of Interest:**
Software Engineering, Artificial Intelligence, Backend Development, and DevOps.

**GitHub:** [Thilini-samanthika](https://github.com/Thilini-samanthika)

**Repository:** [AI Software Engineering Assistant](https://github.com/Thilini-samanthika/AI-Software-Engineering-Assistant)

---

##  Project Purpose

This project was developed for educational purposes, practical exploration of AI technologies, and software engineering portfolio demonstrations.

---

<div align="center">

###  AI Software Engineering Assistant

**Exploring Intelligent Software Development Through Multi-Agent AI**

If you find this project useful, consider giving it a star!

</div>
