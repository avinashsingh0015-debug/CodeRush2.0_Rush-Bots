import os
import requests
import json
from dotenv import load_dotenv

# Load the variables from the .env file into the system
load_dotenv()

class LLMAdapter:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        
        # Swapped to a highly reliable free model
        self.model = "inclusionai/ling-3.0-tiny:free"
    def generate_patch(self, system_prompt: str, user_prompt: str) -> str:
        """Sends the context to the LLM and returns the suggested code fix."""
        
        if not self.api_key:
            return "Error: OPENROUTER_API_KEY environment variable is missing."

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/limaytidke/CodehernessV2", 
            "X-Title": "CodeHarness V2"
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.1 
        }

        try:
            response = requests.post(self.api_url, headers=headers, data=json.dumps(payload))
            
            # This will now catch and print the EXACT message from OpenRouter if it fails
            if response.status_code != 200:
                return f"API Error {response.status_code}: {response.text}"
            
            result = response.json()
            return result['choices'][0]['message']['content']
            
        except Exception as e:
            return f"Code Execution Error: {str(e)}"

if __name__ == "__main__":
    print("Booting up LLM Adapter...")
    adapter = LLMAdapter()
    
    response = adapter.generate_patch(
        system_prompt="You are a helpful coding assistant.",
        user_prompt="Reply with exactly 'Backend is online!' and nothing else."
    )
    
    print(f"AI Response: {response}")