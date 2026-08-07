from pathlib import Path

def read_repo(folder=".") -> str:
    context = ""
    ignored_dirs = {".git", "harness", "venv", "__pycache__", ".venv"}
    ignored_files = {"main.py", "model_adapter.py", "sandbox.py", "repo_indexer.py", "ui.py"}

    root_path = Path(folder)
    for path in root_path.rglob("*.py"):
        # Check if path is in ignored directory or file list
        if any(part in ignored_dirs for part in path.parts):
            continue
        if path.name in ignored_files or path.name.startswith("test_"):
            continue

        try:
            with open(path, "r", encoding="utf-8") as f:
                context += f"\n--- File: {path.relative_to(root_path)} ---\n" + f.read()
        except Exception as e:
            continue

    return context
