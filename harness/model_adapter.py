import time
import requests

def call_ai(prompt: str, model: str = "qwen2.5-coder:7b"):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2
        }
    }
    
    try:
        # Timeout ko 120 seconds rakhein taaki model heavy generation complete kar sake
        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        generated_code = data.get("response", "")
        return generated_code, 0.0
    except Exception as e:
        print(f"\n[Error] Local Ollama call failed: {e}")
        # Hardcoded function ke bajaaye blank string return karein taaki galat overwrite na ho
        return "", 0.0
