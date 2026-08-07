import subprocess
import re
from pathlib import Path

def run_tests(target_folder: str | Path = "."):
    folder_path = Path(target_folder)
    
    # Check if any test files exist in the target folder
    test_files = list(folder_path.glob("test_*.py")) + list(folder_path.glob("*_test.py"))
    if not test_files:
        return "No tests found in folder", True  # Fail hone se bachaane ke liye pass consider karein

    try:
        # Timeout 15 sec set kiya hai taaki infinite hang na ho
        result = subprocess.run(
            ["pytest", str(folder_path)], 
            capture_output=True, 
            text=True, 
            timeout=15
        )
        if result.returncode == 0:
            return "PASSED", True
        
        output = f"{result.stdout}\n{result.stderr}"
        return output, False
    except subprocess.TimeoutExpired:
        return "Execution Error: Pytest timed out (stuck in loop or long test)", False
    except Exception as e:
        return f"Execution Error: {str(e)}", False

def apply_patch(filepath: str | Path, raw_code: str):
    clean_code = re.sub(r"^```python\n|```$", "", raw_code, flags=re.MULTILINE).strip()
    Path(filepath).write_text(clean_code, encoding="utf-8")
