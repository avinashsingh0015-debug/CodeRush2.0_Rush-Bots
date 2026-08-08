# services/verifier.py
import subprocess
import os

class CodeVerifier:
    def __init__(self, target_directory="."):
        self.target_directory = os.path.abspath(target_directory)

    def run_tests(self, test_file_name=None) -> dict:
        """
        Runs pytest for a specific test file or the whole directory.
        """
        try:
            env = os.environ.copy()
            env["PYTHONPATH"] = self.target_directory

            cmd = ["pytest", "-q", "--tb=short"]
            
            # Specific test file targeting to isolate tests
            if test_file_name:
                test_path = os.path.join(self.target_directory, "test", test_file_name)
                if os.path.exists(test_path):
                    cmd.append(test_path)

            result = subprocess.run(
                cmd,
                cwd=self.target_directory,
                capture_output=True,
                text=True,
                env=env,
                timeout=30
            )

            return {
                "success": (result.returncode == 0),
                "output": (result.stdout if result.stdout else result.stderr).strip()
            }
        except Exception as e:
            return {"success": False, "output": str(e)}
