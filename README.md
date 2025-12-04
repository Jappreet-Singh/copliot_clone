# 🚀 AI Chatbot (Angular + FastAPI + Ollama)

A local, free AI chatbot (similar to ChatGPT) using:

- Frontend: Angular 20
- Backend: FastAPI (Python)
- AI Engine: Ollama (local LLM such as Llama 3)

Run the model on your device with no API costs and no internet required after installation.

## 📦 Features

- Real-time AI chat (User → FastAPI → Ollama → Response)
- Local LLM (free forever via Ollama)
- Fast, lightweight FastAPI backend
- Angular UI with user and AI message types
- Fully extensible (history, streaming, auth, multiple models)

## 🛠️ Tech Stack

- Frontend: Angular 20
- Backend: FastAPI (Python 3)
- AI Engine: Ollama (e.g., Llama 3)
- Communication: REST (HTTP POST)

## 📥 Installation & Setup

1. Install Ollama
   - Download: https://ollama.com/download
   - Pull a model (example):
     ```bash
     ollama pull llama3
     ```
   - Test:
     ```bash
     ollama run llama3
     ```

2. Backend (FastAPI)
   ```bash
   pip install fastapi uvicorn ollama
   uvicorn copilotApi:app --reload --port 8000
   ```
   API available at: http://localhost:8000

3. Frontend (Angular)
   ```bash
   npm install
   ng serve
   ```
   Angular runs at: http://localhost:4200

Make sure CORS allows Angular to communicate with FastAPI.

## 📡 API

POST /chat

Request:
```json
{ "message": "Hello AI!" }
```

Response:
```json
{ "response": "Hello! How can I help you today?" }
```

## 🧠 How It Works

1. User types a message in Angular UI.  
2. Angular sends the message to FastAPI (HttpClient).  
3. FastAPI forwards the message to Ollama (e.g., `ollama.chat()` in Python).  
4. Model responds and FastAPI returns the response to Angular.  
5. Angular displays the AI message.

// ...existing code...
## 📁 Project Structure

- /src
  - index.html
  - main.ts
  - styles.css
  - /app
    - app.config.ts
    - app.css
    - app.html
    - app.routes.ts
    - app.spec.ts
    - app.ts
    - /backend
      - copilotApi.py
    - /copilot-ui
      - copilot-ui.css
      - copilot-ui.html
      - copilot-ui.spec.ts
      - copilot-ui.ts
- README.md

## 🧪 Example Flow

You: "Explain what Angular signals are."  
Angular → FastAPI → Ollama → AI: "Signals in Angular are reactive primitives that track state…"

## 🔧 Configuration

Change model in backend:
```py
model = "llama3"
```
Other examples: `phi3`, `mistral`, `llama2`, `deepseek-coder`, `qwen2`

## 🧱 Future Improvements

- Streaming responses (token-by-token)
- Save chat history in a database
- Multiple model selection
- User accounts & authentication
- Improved UI (Bootstrap / Tailwind)

## 🤝 Contributing
Pull requests welcome. Open an issue for feature requests.

## 📜 License
This project is free to use under the MIT license.
