import requests
import json

def test_ollama_connection():
    url = 'http://localhost:11434/api/generate'
    payload = {
        'model': 'phi3',
        'prompt': 'Say hello',
        'stream': False,
        'options': {
            'num_ctx': 1024,
            'num_predict': 150
        }
    }

    try:
        response = requests.post(url, json=payload)
        print(f'Status Code: {response.status_code}')
        if response.status_code == 200:
            result = response.json()
            print(f'Response: {result.get("response", "No response field")}')
        else:
            print(f'Error: {response.text}')
    except Exception as e:
        print(f'Exception: {e}')

if __name__ == "__main__":
    test_ollama_connection()