import requests
import json
import os

def generate_llm_response(prompt: str) -> str:
    """
    Send prompt to Ollama REST API and return the generated response.
    
    Args:
        prompt (str): The input prompt to send to the LLM
        
    Returns:
        str: The generated response from the LLM
    """
    # Check if we're in debug/fallback mode
    if os.getenv("JARVIS_FALLBACK_MODE", "").lower() == "true":
        # Fallback mode for when Ollama is unavailable or out of memory
        return f"I received your query: '{prompt[:50]}...' and would normally process this with the LLM, but I'm currently running in fallback mode due to resource constraints."
    
    url = "http://localhost:11434/api/generate"
    
    # Try with memory-optimized settings first
    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_ctx": 512,    # Minimal context to save memory
            "num_predict": 100, # Shorter predictions to save memory
            "temperature": 0.7,
            "top_p": 0.9
        }
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        result = response.json()
        return result.get('response', '')
    except requests.exceptions.HTTPError as e:
        if response.status_code == 500:
            error_detail = response.json().get('error', '')
            if 'memory' in error_detail.lower() or 'available' in error_detail.lower():
                return "Sorry, the model requires more memory than available. Please close other applications and try again, or set JARVIS_FALLBACK_MODE=true to use fallback responses."
            else:
                return f"Server error: {error_detail}"
        print(f"HTTP Error communicating with Ollama: {e}")
        return "Sorry, I'm unable to generate a response right now."
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with Ollama: {e}")
        return "Sorry, I'm unable to generate a response right now."