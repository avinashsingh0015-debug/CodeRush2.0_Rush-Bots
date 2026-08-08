import os

class RepoScanner:
    def __init__(self, target_directory: str):
        self.target_directory = target_directory

    def gather_context(self, file_extension: str = ".py") -> str:
        """
        Walks through the target directory, reads all files with the given extension,
        and combines them into a single string for the LLM to read.
        """
        if not os.path.exists(self.target_directory):
            return f"Error: Directory '{self.target_directory}' does not exist."

        code_context = f"Project Context from {self.target_directory}:\n\n"
        
        for root, dirs, files in os.walk(self.target_directory):
            # Skip hidden folders like .git or __pycache__
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != "__pycache__"]
            
            for file in files:
                if file.endswith(file_extension):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            file_contents = f.read()
                            # Format it cleanly so the AI knows which file it is looking at
                            code_context += f"========== FILE: {file_path} ==========\n"
                            code_context += f"{file_contents}\n\n"
                    except Exception as e:
                        code_context += f"Could not read {file_path}: {str(e)}\n"
                        
        return code_context

if __name__ == "__main__":
    # Let's test it by having it scan its own services folder!
    print("Booting up Repo Scanner...")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    scanner = RepoScanner(target_directory=current_dir)
    context_output = scanner.gather_context(file_extension=".py")
    
    print(context_output)