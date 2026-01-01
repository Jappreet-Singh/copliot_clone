# 🚀 AI Chatbot with RAG (Angular + FastAPI + Ollama)

A **fully local, free AI chatbot** with **Retrieval-Augmented Generation (RAG)**, similar to ChatGPT, built using Angular, FastAPI, and Ollama.

Runs **entirely on your machine** — no paid APIs, no token limits, and no internet required after setup.

---

## 🎯 Project Overview

This project demonstrates a **production-style AI system** using:
- Angular (frontend)
- FastAPI (backend)
- Ollama (local LLM)
- ChromaDB (vector database for RAG)

The chatbot can:
- Answer general questions
- Ingest documents (PDF / TXT)
- Retrieve relevant context from documents
- Generate grounded, context-aware responses

---

## 📦 Features

- Real-time AI chat
- Streaming responses (token-by-token)
- **Retrieval-Augmented Generation (RAG)**
- Document upload (PDF / TXT)
- Local vector database (ChromaDB)
- Local embeddings via Ollama
- No API keys or usage limits
- FastAPI backend with streaming
- Angular chat UI
- Modular and extensible architecture

---

## 🛠️ Tech Stack

### Frontend
- Angular 20
- TypeScript
- HttpClient

### Backend
- FastAPI (Python 3.11)
- Uvicorn

### AI & RAG
- Ollama (local LLM)
- LangChain
- ChromaDB
- Ollama Embeddings

### Supported Models
- `llama3`
- `phi3`
- `mistral`
- `qwen2`
- `deepseek-coder`

---

## 🧠 How RAG Works

1. User uploads a document (PDF or TXT)
2. Backend extracts text
3. Text is chunked and embedded
4. Embeddings are stored in ChromaDB
5. User asks a question
6. Relevant chunks are retrieved via similarity search
7. Retrieved context is injected into the system prompt
8. Ollama generates a grounded response

---

## 📥 Installation & Setup

### 1️⃣ Install Ollama

Download: https://ollama.com/download

### 📥 Model Setup

Pull a model:
```bash
ollama pull llama3 

test model:
ollama run llama3

### Backend Setup(FastApi)

- python -m venv venv venv\Scripts\activate
- pip install fastapi uvicorn ollama \
  langchain langchain-ollama langchain-chroma \
  chromadb pymupdf python-multipart

test backend:
uvicorn chatApi:app --reload

### Frontend Setup(Angular)

- npm install
- npg serve
-should run it on http://localhost:4200 because of CORS

## 📡 API Endpoints

### POST /message

Streaming AI chat response.

Request
{
  "message": "Explain the uploaded document"
}

Response
(streamed text/plain)

### POST /uploadfile

Upload a document for RAG ingestion.

Supported formats
.pdf
.txt

Response

{
  "filename": "example.pdf",
  "summary": "High-level document summary..."
}

## 📁 Project Structure
  /src/
  └─ app/
  │  │  ├─ backend/
  │  │  │  ├─ chatApi.py
  │  │  │  ├─ chroma_db/
  │  │  │  ├─ uploads/
  │  │  │  ├─ upload_file/
  │  │  │  │ └─ upload_file.py
  │  │  │  └─ rag/
  │  │  │     ├─ ingest.py
  │  │  │     ├─ query.py
  │  │  │     └─ vectorStorage.py
  │  │  ├─ chat/
  │  │  │  ├─ chat.ts
  │  │  │  ├─ chat.html
  │  │  │  └─ chat.css
  │  │  ├─  app.config.ts
  │  │  ├─ app.css
  │  │  ├─ app.html
  │  │  ├─ app.routes.ts
  │  │  ├─ app.spec.ts
  │  │  └─ app.ts
  │  ├─ index.html
  │  ├─ main.ts
  │  └─ styles.css
  ├─ .editorconfig
  ├─ .gitignore
  ├─ angular.json
  ├─ package.json
  ├─ package-lock.json
  ├─ README.md
  ├─ tsconfig.app.json
  ├─ tsconfig.json
  └─ tsconfig.spec.json
      
      
## 🧪 Example Usage

Upload a document:
company_policy.pdf

Ask:
“What does the document say about vacation policy?”

The AI responds using retrieved document context.

## 🔧 Configuration

Change the model in the backend:
model = "llama3"

Other supported models:
phi3
mistral
qwen2
deepseek-coder

## 🧱 Completed Phases

Phase 1: Angular UI & FastAPI setup

Phase 2: Local LLM integration with Ollama

Phase 3: RAG system with document ingestion and vector search 