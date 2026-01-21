from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag import RAGSystem
from llm import generate_llm_response
import os

# Initialize FastAPI app
app = FastAPI(title="Jarvis AI Assistant API", version="1.0.0")

# Initialize RAG system
# Note: Pinecone API key should be set as environment variable PINECONE_API_KEY
rag_system = RAGSystem(pinecone_api_key=os.getenv("PINECONE_API_KEY"))

# Define request/response models
class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    answer: str

@app.on_event("startup")
async def startup_event():
    """
    Load the knowledge document into the RAG system on startup.
    """
    try:
        import os
        # Get the directory where this app.py file is located
        current_dir = os.path.dirname(os.path.abspath(__file__))
        knowledge_file_path = os.path.join(current_dir, "..", "data", "knowledge.txt")
        rag_system.load_and_process_document(knowledge_file_path)
        print("Knowledge base loaded successfully!")
    except Exception as e:
        print(f"Error loading knowledge base: {e}")

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Chat endpoint that takes user query and returns AI-generated response.
    
    Args:
        request (ChatRequest): Contains the user query
        
    Returns:
        ChatResponse: Contains the AI-generated answer
    """
    try:
        # Generate answer using RAG system
        answer = rag_system.generate_answer(request.query, generate_llm_response)
        
        return ChatResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.get("/")
async def root():
    """
    Health check endpoint.
    """
    return {"message": "Jarvis AI Assistant API is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)