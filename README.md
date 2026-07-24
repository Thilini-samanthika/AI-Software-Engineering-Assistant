# 🤖 AI Software Engineering Assistant

> A Multi-Agent AI System for Software Developers built with LangGraph, LangChain, Groq, ChromaDB, and Streamlit.

---

## 📖 Project Overview

AI Software Engineering Assistant is an intelligent multi-agent system designed to help software developers with day-to-day software engineering tasks.

Instead of searching across multiple websites such as Python Docs, Microsoft Learn, GitHub Docs, Stack Overflow, and other documentation sources, developers can ask questions through a single AI assistant.

The system uses multiple specialized AI agents, Retrieval-Augmented Generation (RAG), and a Reflection Agent to generate accurate and well-structured responses.

---

## 🚀 Features

### 💻 Coding Agent
- Explain source code
- Debug errors
- Suggest bug fixes
- Optimize code
- Generate Unit Tests
- Explain algorithms

### 📄 Documentation Agent
- Generate README files
- Generate API Documentation
- Generate Function Comments
- Create Project Documentation

### 📚 RAG Agent
- Search Software Engineering documentation
- Retrieve relevant knowledge
- Answer questions using PDF knowledge base

### 🧠 Reflection Agent
- Review generated answers
- Improve response quality
- Verify correctness before returning the final answer

---

## 🏗️ Multi-Agent Architecture

```text
                User
                  │
          Streamlit Interface
                  │
             Router Agent
                  │
     ┌──────────┼──────────┐
     ▼          ▼          ▼
 Coding     Documentation   RAG
  Agent        Agent       Agent
      \          |          /
       \         |         /
        ▼        ▼        ▼
        Reflection Agent
               │
        Final Response
```

---

## 🤖 Agentic AI Patterns

This project implements multiple Agentic AI patterns:

- ✅ Router Pattern
- ✅ ReAct Pattern
- ✅ Tool Use
- ✅ Reflection Pattern

---

## 🛠️ Technologies Used

| Category | Technology |
|----------|------------|
| Language | Python |
| Frontend | Streamlit |
| Multi-Agent | LangGraph |
| LLM Framework | LangChain |
| Model | Groq (Llama 3.1) |
| Embeddings | Sentence Transformers |
| Vector Database | ChromaDB |
| PDF Loader | PyPDFLoader |
| Environment | python-dotenv |
| Version Control | Git & GitHub |

---

## 📁 Project Structure

```text
AI-Software-Engineering-Assistant/

│── app.py
│── requirements.txt
│── README.md
│── .env
│── .gitignore
│
├── agents/
│   ├── router.py
│   ├── coding_agent.py
│   ├── documentation_agent.py
│   ├── rag_agent.py
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
│   └── vector_store.py
│
├── data/
│   └── pdfs/
│
└── chroma_db/
```

---

## 📚 Knowledge Base

The RAG system uses Software Engineering documents including:

- Python Documentation
- C# Documentation
- Java Documentation
- SOLID Principles
- OOP Notes
- Clean Code
- Design Patterns
- REST API Guide
- Git Documentation
- GitHub Documentation
- SQL Notes
- Unit Testing Guide
- Agile Guide
- Scrum Guide
- Software Architecture
- Refactoring Guide
- Docker Basics
- Kubernetes Basics
- Microservices
- CI/CD Notes

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Software-Engineering-Assistant.git
```

### 2. Move into the project

```bash
cd AI-Software-Engineering-Assistant
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Create a `.env` file

```env
GROQ_API_KEY=your_api_key_here
OPENROUTER_API_KEY=your_api_key_here
```

### 7. Build the Vector Database

```bash
python test_rag.py
```

### 8. Run the application

```bash
streamlit run app.py
```

---

## 💬 Example Questions

- Explain SOLID Principles
- Explain the Singleton Design Pattern
- Generate a README for my project
- Debug my Python code
- Explain this C# code
- Generate Unit Tests
- Explain REST API
- What is Dependency Injection?

---

## 📸 Screenshots

### Home Page

_Add a screenshot here_

### Chat Interface

_Add a screenshot here_

### Agent Dashboard

_Add a screenshot here_

### Retrieved Documents

_Add a screenshot here_

---

## 🌟 Future Improvements

- Multiple LLM Support
- PDF Upload
- Conversation Memory
- User Authentication
- Voice Input
- AI Code Review
- Docker Deployment
- Cloud Deployment
- Feedback System

---

## 👩‍💻 Author

**Thilini Samanthika**

Software Engineering Student

---

## 📄 License

This project is developed for educational purposes.