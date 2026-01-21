from sentence_transformers import SentenceTransformer
from typing import List

class EmbeddingGenerator:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the embedding generator with a pre-trained model.
        
        Args:
            model_name (str): Name of the SentenceTransformer model to use
        """
        self.model = SentenceTransformer(model_name)
    
    def generate_embeddings(self, text_chunks: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of text chunks.
        
        Args:
            text_chunks (List[str]): List of text chunks to embed
            
        Returns:
            List[List[float]]: List of embedding vectors
        """
        embeddings = self.model.encode(text_chunks)
        # Convert to list of lists for JSON serialization
        return embeddings.tolist()

    def generate_single_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text (str): Text to embed
            
        Returns:
            List[float]: Embedding vector
        """
        embedding = self.model.encode([text])
        return embedding[0].tolist()