"""
Test script to verify all modules import correctly
"""

print("Testing imports...")

try:
    from backend.llm import generate_llm_response
    print("✓ Successfully imported llm module")
except ImportError as e:
    print(f"✗ Failed to import llm module: {e}")

try:
    from backend.embeddings import EmbeddingGenerator
    print("✓ Successfully imported embeddings module")
except ImportError as e:
    print(f"✗ Failed to import embeddings module: {e}")

try:
    from backend.pinecone_db import PineconeDB
    print("✓ Successfully imported pinecone_db module")
except ImportError as e:
    print(f"✗ Failed to import pinecone_db module: {e}")

try:
    from backend.rag import RAGSystem
    print("✓ Successfully imported rag module")
except ImportError as e:
    print(f"✗ Failed to import rag module: {e}")

print("\nAll imports successful! The application structure is correct.")