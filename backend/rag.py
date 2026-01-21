from typing import List
import sys
import os
# Add the backend directory to the path so imports work correctly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from embeddings import EmbeddingGenerator
from pinecone_db import PineconeDB

class RAGSystem:
    def __init__(self, pinecone_api_key: str = None):
        """
        Initialize the RAG system with embedding generator and Pinecone DB.
        
        Args:
            pinecone_api_key (str): Pinecone API key
        """
        self.embedding_gen = EmbeddingGenerator()
        self.pinecone_db = PineconeDB(api_key=pinecone_api_key)
        self.pinecone_db.create_index(dimension=384)  # all-MiniLM-L6-v2 outputs 384-dim vectors
    
    def load_and_process_document(self, file_path: str, chunk_size: int = 500, overlap: int = 50):
        """
        Load document, chunk it, generate embeddings, and store in Pinecone.
        
        Args:
            file_path (str): Path to the knowledge document
            chunk_size (int): Size of each text chunk
            overlap (int): Overlap between chunks
        """
        # Read the document
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Chunk the text
        chunks = self._chunk_text(text, chunk_size, overlap)
        
        # Generate embeddings
        embeddings = self.embedding_gen.generate_embeddings(chunks)
        
        # Prepare data for Pinecone
        vectors_data = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            vectors_data.append({
                'id': f'chunk_{i}',
                'values': embedding,
                'metadata': {'text': chunk}
            })
        
        # Store in Pinecone
        self.pinecone_db.upsert_vectors(vectors_data)
    
    def _chunk_text(self, text: str, chunk_size: int, overlap: int) -> List[str]:
        """
        Split text into overlapping chunks.
        
        Args:
            text (str): Text to chunk
            chunk_size (int): Size of each chunk
            overlap (int): Overlap between chunks
            
        Returns:
            List[str]: List of text chunks
        """
        chunks = []
        start = 0
        text_len = len(text)
        
        while start < text_len:
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            
            # Move start position by (chunk_size - overlap) to create overlap
            start += chunk_size - overlap
            
            # Ensure we don't go beyond the text length
            if start >= text_len:
                # If we've reached the end and haven't included the last bit, add it
                if end < text_len:
                    chunks.append(text[end:text_len])
                break
        
        return chunks
    
    def retrieve_context(self, query: str, top_k: int = 5) -> str:
        """
        Retrieve relevant context from Pinecone based on the query.
        
        Args:
            query (str): Query to search for
            top_k (int): Number of top matches to retrieve
            
        Returns:
            str: Concatenated context from retrieved documents
        """
        # Generate embedding for the query
        query_embedding = self.embedding_gen.generate_single_embedding(query)
        
        # Query Pinecone
        matches = self.pinecone_db.query_similar(query_embedding, top_k)
        
        # Extract text from matches
        context_parts = []
        for match in matches:
            text = match['metadata'].get('text', '')
            if text:
                context_parts.append(text)
        
        # Concatenate context parts
        return ' '.join(context_parts)
    
    def generate_answer(self, query: str, llm_generate_func) -> str:
        """
        Generate an answer using retrieved context and LLM.
        
        Args:
            query (str): User query
            llm_generate_func: Function to call the LLM
            
        Returns:
            str: Generated answer
        """
        # Retrieve context
        context = self.retrieve_context(query)
        
        # Build prompt
        prompt = f"""You are a helpful enterprise AI assistant.

Use ONLY the following context to answer.

Context:
{context}

Question:
{query}

Answer clearly and concisely."""
        
        # Generate response using LLM
        return llm_generate_func(prompt)