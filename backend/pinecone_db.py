from pinecone import Pinecone, PodSpec
from typing import List, Dict, Any
import os

class PineconeDB:
    def __init__(self, api_key: str = None):
        """
        Initialize Pinecone database connection.
        
        Args:
            api_key (str): Pinecone API key
        """
        api_key = api_key or os.getenv("PINECONE_API_KEY")
        if not api_key:
            raise ValueError("Pinecone API key is required. Set PINECONE_API_KEY environment variable.")
        
        self.pc = Pinecone(api_key=api_key)
        self.index_name = "jarvis-knowledge-base"
        
    def create_index(self, dimension: int = 384):
        """
        Create a Pinecone index if it doesn't exist.
        
        Args:
            dimension (int): Dimension of the vectors to store
        """
        # Check if index exists
        indexes = [index['name'] for index in self.pc.list_indexes()]
        if self.index_name not in indexes:
            # Create index - using serverless spec for free tier
            self.pc.create_index(
                name=self.index_name,
                dimension=dimension,
                metric='cosine',
                spec={'serverless': {'region': 'us-east-1', 'cloud': 'aws'}}
            )
        
        # Get index
        self.index = self.pc.Index(self.index_name)
    
    def upsert_vectors(self, vectors_data: List[Dict[str, Any]]):
        """
        Upsert vectors to the Pinecone index.
        
        Args:
            vectors_data: List of dictionaries containing vector data in format:
                         {
                             'id': 'vector_id',
                             'values': [embedding_vector],
                             'metadata': {'text': 'original_chunk'}
                         }
        """
        self.index.upsert(vectors=vectors_data)
    
    def query_similar(self, query_vector: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Query similar vectors from the Pinecone index.
        
        Args:
            query_vector: The query vector to find similar items
            top_k: Number of top similar items to return
            
        Returns:
            List of dictionaries containing matches with metadata
        """
        response = self.index.query(
            vector=query_vector,
            top_k=top_k,
            include_metadata=True
        )
        return response['matches']
    
    def delete_index(self):
        """
        Delete the Pinecone index (useful for cleanup/recreation).
        """
        indexes = [index['name'] for index in self.pc.list_indexes()]
        if self.index_name in indexes:
            self.pc.delete_index(self.index_name)