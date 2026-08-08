# services/parser.py
import re

class CodeParser:
    @staticmethod
    def extract_code(raw_response: str) -> str:
        if not raw_response:
            return ""

        # Markdown ```python ... ``` block extract karein
        pattern = r"```(?:python)?\s*\n(.*?)\n```"
        matches = re.findall(pattern, raw_response, re.DOTALL)

        if matches:
            code = matches[0].strip()
        else:
            # Code block tag nahi mila toh pure text return karein
            code = raw_response.strip()

        # Stray '...' lines remove karein
        clean_lines = [line for line in code.splitlines() if line.strip() != "..."]
        return "\n".join(clean_lines)
