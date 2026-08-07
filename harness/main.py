from pathlib import Path
from ui import HarnessUI
from repo_indexer import read_repo
from sandbox import run_tests, apply_patch
from model_adapter import call_ai

def process_selected_folders(selected_folders: list[Path]):
    if not selected_folders:
        return "No targets selected.", 0.0

    total_cost = 0.0
    processed_summary = []

    for folder in selected_folders:
        try:
            code_context = read_repo(folder)
            if not code_context.strip():
                processed_summary.append(f"{folder.name}: (empty or no valid .py files)")
                continue

            test_result, is_passed = run_tests(folder)

            if not is_passed:
                py_files = [
                    p for p in folder.glob("*.py") 
                    if not p.name.startswith("test_") and not p.name.startswith(".")
                ]

                if not py_files:
                    processed_summary.append(f"⚠️ {folder.name}: No target .py file found")
                    continue

                target_file = py_files[0]

                # Detailed Prompt specifying exact requirements
                prompt = (
                    "You are an expert Python code fixing assistant.\n"
                    f"Target File: {target_file.name}\n\n"
                    f"=== CURRENT FILE CONTENT & REPO CONTEXT ===\n{code_context}\n\n"
                    f"=== TEST FAILURE LOGS ===\n{test_result}\n\n"
                    "INSTRUCTIONS:\n"
                    "1. Fix the logical errors in the target file so all pytest unit tests pass.\n"
                    "2. Preserve the exact function names expected by the test cases.\n"
                    "3. Return ONLY valid, complete Python code for the file. DO NOT wrap code in markdown backticks or add introductory text."
                )

                fixed_code, cost = call_ai(prompt)
                total_cost += cost

                if not fixed_code.strip():
                    processed_summary.append(f"✖ {folder.name}: AI failed to generate code")
                    continue

                apply_patch(target_file, fixed_code)
                
                final_test, final_passed = run_tests(folder)
                if final_passed:
                    processed_summary.append(f"✔ {folder.name} ({target_file.name}): Fixed & Verified")
                else:
                    processed_summary.append(f"✖ {folder.name}: Patch failed verification")
            else:
                processed_summary.append(f"✔ {folder.name}: Passed initial tests")

        except Exception as e:
            processed_summary.append(f"❌ Error processing {folder.name}: {str(e)}")

    summary_text = "\n".join(processed_summary)
    return summary_text, total_cost


if __name__ == "__main__":
    app = HarnessUI(run_harness_callback=process_selected_folders)
    app.run()
