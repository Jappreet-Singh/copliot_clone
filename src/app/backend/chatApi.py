from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
import ollama
from pydantic import BaseModel

app = FastAPI(
    title="AI Chatbot API",
    description="Local AI chatbot backend using FastAPI and Ollama",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["GET","POST"],
    allow_headers=["*"],)

class ChatRequest(BaseModel):
    messages: list  # [{role: "user", content: "..."}]

@app.post("/chat")
def chat_with_ai(req: ChatRequest = Body(..., title="Ollama", description="Chat request with messages")):
    response = ollama.chat(
        model="llama3",
        messages=req.messages
    )
    return {"response": response["message"]["content"]}