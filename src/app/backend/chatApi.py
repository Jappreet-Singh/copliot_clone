import os
import time
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from upload_file.upload_file import extract_text_from_pdf, extract_text_from_txt
from rag.ingest import ingest_text
from rag.query import retrieve_context

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()

# We no longer need the lifespan warmup for Ollama since Gemini is a cloud API.
app = FastAPI(
    title="AI Chatbot API",
    description="Local AI chatbot backend using FastAPI and Groq",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://project-djxlw.vercel.app", "http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Stores the entire conversation (simple in-memory history)
conversation_history = [{
    "role": "system",
    "content": "Respond in very short answers. Max 2 sentences."
}]

# Initialize Groq LLM
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.4,
    max_tokens=100
)

class ChatMessage(BaseModel):
    message: str

@app.post("/message")
def put_message(data: ChatMessage):
    global conversation_history
    t0 = time.time()
    user_message = data.message

    # Add user message to history
    conversation_history.append({
        "role": "user",
        "content": user_message
    })
    
    # RAG WORK BEFORE STREAMING
    try:
        context = retrieve_context(user_message)
        print("RAG time:", time.time()-t0)
    except Exception as e:
        # Fail safely BEFORE headers are sent
        return {"error": f"RAG retrieval failed: {e}"}

    def generate():
        system_prompt = f"""
        You are a personal AI groq.
        Answer using the provided context when relevant.

        Context:
        {context}
        """
        
        # Build Langchain message format
        messages = [SystemMessage(content=system_prompt)]
        for msg in conversation_history:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))

        t1 = time.time()
        print("Groq start delay:", time.time()-t1)
        
        full_reply = ""
        try:
            # Stream chunks back to frontend using LangChain Groq interface
            for chunk in llm.stream(messages):
                if chunk.content:
                    full_reply += chunk.content
                    yield chunk.content
        except Exception as e:
            yield f"\n[Error during response generation: {e}]"

        finally:
            # After stream ends → save assistant reply to history
            conversation_history.append({
                "role": "assistant",
                "content": full_reply
            })

    return StreamingResponse(generate(), media_type="text/plain")


# PHASE 3 PDF extraction endpoint

# TO STORE FILES TEMPORARILY
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def summarize_text(text: str) -> str:
    prompt = f"Summarize the following text clearly:\n\n{text[:6000]}"
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"Error summarizing text: {e}"

@app.post("/uploadfile")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename or "uploaded_file")

    # Save uploaded file temporarily
    with open(file_path, "wb") as f:
        f.write(await file.read())

    try:
        # Extract text
        filename_lower = str(file.filename).lower()
        if filename_lower.endswith(".pdf"):
            extracted_text = extract_text_from_pdf(file_path)
        elif filename_lower.endswith(".txt"):
            extracted_text = extract_text_from_txt(file_path)
        else:
            return {"error": "Unsupported file type"}

        if not extracted_text.strip():
            return {"error": "No text extracted from file"}
        
        # Ingest text into RAG system (Vector DB)
        ingest_text(text=extracted_text, source=str(file.filename))

        # Summarize
        summary = summarize_text(extracted_text)

        return {
            "filename": file.filename,
            "summary": summary
        }
    finally:
        # CLEANUP: Delete the file after it's processed so we don't use disk space
        if os.path.exists(file_path):
            os.remove(file_path)
