from fastapi import FastAPI,Path, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["GET","POST"],
    allow_headers=["*"],)

@app.get("/")
def read_copilot():
    return {"message": "Welcome to the Copilot API"}

@app.post("/message")
def put_message(message: str = Query(..., description="The message to be processed")):   
    # Process the message (dummy processing for illustration)
    return {"sent_message": message}