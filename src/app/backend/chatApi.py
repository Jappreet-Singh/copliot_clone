from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import fitz
import ollama
from pydantic import BaseModel
import os

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

#PHASE 3 PDF extraction endpoint

# TO STORE FILES TEMPORARILY
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def extract_text_from_pdf(file_path: str) -> str:
    doc = fitz.open(file_path)
    text=""
    for page in doc :
        text += str(page.get_text())
        doc.close()
    return text

def extract_text_from_txt(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

def summarize_text(text :str)->str:
    response=ollama.chat(
        model="phi3:mini",
        messages=[
            {
                "role": "user",
                "content": f"Summarize the following text clearly:\n\n{text[:6000]}"
            }
        ],
        options={"temperature": 0.3, "max_tokens": 200}
    )
    return response["message"]["content"]

@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename or "uploaded_file")

    # Save uploaded file
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Extract text
    if str(file.filename).lower().endswith(".pdf"):
        extracted_text = extract_text_from_pdf(file_path)
    elif str(file.filename).lower().endswith(".txt"):
        extracted_text = extract_text_from_txt(file_path)
    else:
        return {"error": "Unsupported file type"}

    if not extracted_text.strip():
        return {"error": "No text extracted from file"}

    # Summarize
    summary = summarize_text(extracted_text)

    return {
        "filename": file.filename,
        "summary": summary
    }