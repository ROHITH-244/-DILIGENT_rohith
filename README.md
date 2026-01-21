# Jarvis AI Assistant

A self-hosted RAG-powered AI assistant using LLaMA, Pinecone, and Streamlit.

## Prerequisites

1. **Ollama**: Install Ollama and pull the LLaMA model:
   ```bash
   ollama pull llama3
   ```

2. **Pinecone Account**: Sign up for a Pinecone account and get your API key.

## Setup

1. Install Python dependencies:
   ```bash
   # From the project root directory
   cd backend
   pip install -r requirements.txt
   
   cd ../ui
   pip install -r requirements.txt
   ```

2. Set your Pinecone API key as an environment variable:
   ```bash
   export PINECONE_API_KEY='your-api-key-here'
   ```

## Running the Application

1. Start the backend API server:
   ```bash
   cd backend
   uvicorn app:app --reload
   ```

2. In a separate terminal, start the frontend:
   ```bash
   cd ui
   streamlit run chat_ui.py
   ```

3. Open your browser to `http://localhost:8501` to use the chat interface.

## Architecture

- **Backend**: FastAPI server handling RAG logic
- **LLM**: Self-hosted LLaMA via Ollama
- **Embeddings**: SentenceTransformers for text embeddings
- **Vector DB**: Pinecone for similarity search
- **Frontend**: Streamlit chat interface