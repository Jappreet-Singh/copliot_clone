from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import ollama
from pydantic import BaseModel

#lifespan to warm up ollama model
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Warming up Ollama model...")
    try:
        ollama.chat(
            model="phi3:mini",
            messages=[{"role": "user", "content": "warmup message"}]
        )
        print("Model warmed up successfully.")
    except Exception as e:
        print(f"Error warming up model: {e}")
    
    yield   # ---- FastAPI runs normally after this ----

    print("Shutting down API...")

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

# Stores the entire conversation (simple in-memory history)
conversation_history = [{
        "role": "system",
        "content": "Respond in very short answers. Max 2 sentences."
    },]


# JSON body model
class ChatMessage(BaseModel):
    message: str


@app.post("/message")
def put_message(data: ChatMessage):
    global conversation_history

    user_message = data.message

    # Add user message to history
    conversation_history.append({
        "role": "user",
        "content": user_message
    })

    def generate():
        # Ask Ollama with full conversation
        stream = ollama.chat(
            model="phi3:mini",
            messages=conversation_history,
            stream=True,
            options={"max_tokens": 100, "temperature": 0.4}
        )

        full_reply = ""

        # Stream chunks back to frontend
        for chunk in stream:
            if "message" in chunk:
                content = chunk["message"]["content"]
                if content:
                    full_reply += content
                    yield content  # streaming to frontend

        # After stream ends → save assistant reply to history
        conversation_history.append({
            "role": "assistant",
            "content": full_reply
        })

    return StreamingResponse(generate(), media_type="text/plain")