import re

class CodeParser:
    @staticmethod
    def extract_code(ai_response: str) -> str:
        """
        Strips away conversational text and extracts only the raw Python code.
        """
        if not ai_response:
            return ""
            
        # Look for code hidden inside ```python ... ``` or just ``` ... ```
        match = re.search(r'```(?:python)?(.*?)```', ai_response, re.DOTALL)
        
        if match:
            return match.group(1).strip()
            
        # Fallback: If the AI forgot to use backticks, just return the raw response
        return ai_response.strip()