import subprocess
import os

class CodeVerifier:
    def __init__(self, target_directory: str):
        self.target_directory = target_directory

    def run_tests(self) -> dict:
        """
        Runs the test suite (pytest) in the target directory.
        Captures the terminal output so the AI can read the errors.
        """
        try:
            # We use subprocess to simulate a user typing 'pytest' in the terminal
            result = subprocess.run(
                ["pytest"], 
                cwd=self.target_directory,
                capture_output=True,
                text=True,
                check=False # We want to capture the output even if the tests fail!
            )
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout if result.returncode == 0 else result.stdout + "\n" + result.stderr
            }
            
        except FileNotFoundError:
            return {
                "success": False,
                "output": "Error: 'pytest' command not found. Make sure it is installed."
            }
        except Exception as e:
            return {
                "success": False,
                "output": f"Verification Engine Error: {str(e)}"
            }

if __name__ == "__main__":
    print("Booting up Code Verifier...")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    verifier = CodeVerifier(target_directory=current_dir)
    test_results = verifier.run_tests()
    
    print(f"\nDid the tests pass? {test_results['success']}")
    print(f"Terminal Output:\n{test_results['output']}")