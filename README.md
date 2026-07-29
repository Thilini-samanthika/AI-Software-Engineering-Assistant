#  AI Software Engineering Assistant

> A Multi-Agent AI System for Software Developers built using **LangGraph, LangChain, RAG, ChromaDB, Groq LLM, and Streamlit**.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-success)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red)
![Groq](https://img.shields.io/badge/Groq-LLM-orange)
![License](https://img.shields.io/badge/License-MIT-green)

---
# Live demo link:
https://ai-software-engineering-assistant-ngsqmt5gnqkl3sa2psvwks.streamlit.app/

---

#  Developer

**M.Thilini Samanthika** - **ITBIN-2313-0061**

GitHub:
https://github.com/Thilini-samanthika

---

#  Project Overview

AI Software Engineering Assistant is a Multi-Agent AI application that helps software developers with coding, debugging, software engineering concepts, documentation generation, architecture recommendations, code reviews, and intelligent documentation search using Retrieval-Augmented Generation (RAG).

Instead of searching across multiple websites, developers can ask questions in one place and receive AI-powered answers.

---

#  Features

-  Explain source code
-  Debug programming errors
-  Software engineering documentation search (RAG)
-  Generate README files
-  Generate API documentation
-  Generate Unit Tests
-  System Architecture Recommendations
-  AI Code Review
-  Upload PDF Knowledge Base
-  Search uploaded documents
-  Reflection Agent for answer improvement

---

#  Multi-Agent Architecture

```
                  User
                    │
             Streamlit UI
                    │
             Router Agent
                    │
    ┌────────┬──────────┬─────────────┐
    │        │          │             │
 Coding   Documentation  RAG   Architecture
 Agent      Agent       Agent      Agent
    │
 Testing Agent
    │
 Code Review Agent
    │
 Reflection Agent
    │
          Final Response
```

---

#  Agent Overview

| Agent | Responsibility |
|--------|---------------|
| Router Agent | Selects the correct agent |
| Coding Agent | Code explanation & debugging |
| Documentation Agent | README & API documentation |
| RAG Agent | Searches knowledge base |
| Testing Agent | Generates unit tests |
| Architecture Agent | Recommends software architecture |
| Code Review Agent | Reviews code quality |
| Reflection Agent | Improves final response |

---

#  Knowledge Base

The assistant uses a ChromaDB vector database containing software engineering documentation.

Current documents include:

- Python
- Java
- C#
- SQL
- SOLID Principles
- Object-Oriented Programming
- Design Patterns
- Clean Code
- REST API
- Git
- GitHub
- Docker
- Kubernetes
- Agile
- Scrum
- CI/CD
- Microservices
- Refactoring
- Software Architecture
- Unit Testing

---

#  Technologies Used

## Frontend

- Streamlit

## Backend

- Python

## AI Framework

- LangGraph
- LangChain

## Large Language Model

- Groq (Llama 3)

## Vector Database

- ChromaDB

## Embeddings

- Sentence Transformers

## Document Loader

- PyPDFLoader

---

#  Project Structure

```
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
├── data/
│   ├── pdfs/
│   └── uploads/
│
├── assets/
│
├── app.py
├── requirements.txt
├── README.md
└── .env
```

---

#  Installation

Clone the repository

```bash
git clone https://github.com/Thilini-samanthika/AI-Software-Engineering-Assistant.git
```

Go to the project

```bash
cd AI-Software-Engineering-Assistant
```

Create virtual environment

```bash
python -m venv venv
```

Activate virtual environment

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

#  Environment Variables

Create a `.env` file.

```
GROQ_API_KEY=your_api_key
OPENROUTER_API_KEY=your_api_key
```

---

#  Run the Project

```bash
streamlit run app.py
```

---

#  Application Screenshots

Add screenshots here.

- Home Page
  
<img width="400" height="200" alt="Screenshot 2026-07-26 151559" src="https://github.com/user-attachments/assets/40aa5952-6789-4922-a343-61736040bd1d" />


- Chat Interface
  
<img width="400" height="200" alt="Screenshot 2026-07-26 150713" src="https://github.com/user-attachments/assets/68a02a9a-d21c-4467-a6e9-a37210fe57ac" />


- RAG Search
  
<img width="700" height="100" alt="Screenshot 2026-07-26 150943" src="https://github.com/user-attachments/assets/66fd5958-40ff-479d-a151-37cc53b75f0d" />


- PDF Upload
  
<img width="200" height="400" alt="Screenshot 2026-07-26 150818" src="https://github.com/user-attachments/assets/24beaca4-9c3e-47dd-b48b-748fbab037bd" />

---

#  Example Questions

```
Explain SOLID principles.

Review this Python code.

Generate a README for my project.

Generate unit tests for this function.

Design a Hospital Management System.

Explain the Repository Pattern.

Search Docker documentation.

Summarize the uploaded PDF.
```

---

#  Future Improvements

- Voice Assistant
- AI Pair Programming
- Multiple LLM Support
- Code Execution Sandbox
- UML Diagram Generation
- Database Schema Generator
- Docker Deployment
- Authentication

---

#  License

This project is developed for educational purposes and internship portfolio demonstrations.
