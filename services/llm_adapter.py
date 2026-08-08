# services/llm_adapter.py
import requests

class LLMAdapter:
    def __init__(self, model_name="qwen2.5-coder:3b", ollama_url="http://localhost:11434/api/generate"):
        self.model_name = model_name
        self.ollama_url = ollama_url

    def generate_patch(self, system_prompt: str, user_prompt: str) -> str:
        full_prompt = f"{system_prompt}\n\nUSER TASK:\n{user_prompt}"
        
        payload = {
            "model": self.model_name,
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": 0.1  # Code accuracy ke liye low temperature
            }
        }
        
        try:
            response = requests.post(self.ollama_url, json=payload, timeout=60)
            if response.status_code == 200:
                data = response.json()
                return data.get("response", "")
            else:
                raise Exception(f"Ollama API Error Status: {response.status_code}")
        except Exception as e:
            print(f"❌ LLM Connection Exception: {e}")
            raise e
