import requests
import json

class OllamaClient:
    def __init__(self, model='llama3'):
        self.model = model
        self.api_url = 'http://localhost:11434/api/generate'
        
    def generate(self, prompt):
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()
            result = response.json()
            return result.get('response', '').strip()
        except requests.exceptions.RequestException as e:
            return f"Error communicating with Ollama: {str(e)}"
        except json.JSONDecodeError:
            return "Error: Invalid response from Ollama"
