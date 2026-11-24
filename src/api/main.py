
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from src.retrieval.rag_chatbot import ask_question

app=FastAPI(title="Training Center RAG Chatbot API",description="API for the existing RAG chatbot",version="1.0.0")

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        description="The user's question"
    )
@app.post("/chat")#بنشئ endpoint 
def chat(request: ChatRequest):

    try:
        result = ask_question(request.question)

        return {
            "answer": result["answer"],
            "sources": result["sources"],
            "supported": result["supported"]
        }

    except Exception as e:
        print(f"DEBUG ERROR: {repr(e)}")

        raise HTTPException(
        status_code=500,
        detail="An internal error occurred while processing the question."
    )