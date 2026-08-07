import os
import time
from services.scanner import RepoScanner
from services.llm_adapter import LLMAdapter
from services.verifier import CodeVerifier
from services.parser import CodeParser
from services.patcher import FilePatcher

def safe_generate_patch(adapter, system_prompt, user_prompt, max_retries=5, initial_delay=5):
    """
    Calls LLMAdapter with exponential backoff to handle Rate Limit (429) errors gracefully.
    """
    delay = initial_delay
    for attempt in range(1, max_retries + 1):
        try:
            return adapter.generate_patch(system_prompt, user_prompt)
        except Exception as e:
            error_msg = str(e).lower()
            # Check for common rate limit indicators
            if "429" in error_msg or "rate limit" in error_msg or "resource_exhausted" in error_msg:
                print(f"⚠️ Rate limit hit (Attempt {attempt}/{max_retries}). Waiting {delay} seconds before retrying...")
                time.sleep(delay)
                delay *= 2  # Exponential backoff (5s -> 10s -> 20s...)
            else:
                # If it's another non-rate-limit error, re-raise it
                raise e
                
    print("❌ Failed to get response from LLM after maximum rate-limit retries.")
    return None

def start_agent_loop():
    print("🚀 Starting CodeHarness V2 Agent...\n")
    
    target_dir = os.path.dirname(os.path.abspath(__file__))
    app_dir = os.path.join(target_dir, "app")
    
    scanner = RepoScanner(target_directory=app_dir)
    adapter = LLMAdapter()
    verifier = CodeVerifier(target_directory=target_dir)
    
    app_files = [
        f for f in os.listdir(app_dir) 
        if f.endswith(".py") and not f.endswith("_fixed.py")
    ]

    if not app_files:
        print("No target Python files found in the 'app' directory.")
        return

    print(f"Found {len(app_files)} file(s) to process: {', '.join(app_files)}\n")

    for file_index, file_name in enumerate(app_files, 1):
        app_file_path = os.path.join(app_dir, file_name)
        base_name, ext = os.path.splitext(file_name)
        fixed_file_path = os.path.join(app_dir, f"{base_name}_fixed{ext}")
        
        print(f"\n==================================================")
        print(f"🎯 [{file_index}/{len(app_files)}] Processing file: {file_name}")
        print(f"==================================================")

        max_attempts = 3
        attempt = 1
        
        while attempt <= max_attempts:
            print(f"\n--- ATTEMPT {attempt}/{max_attempts} for {file_name} ---")
            print("[1/5] Gathering code context...")
            
            # Read single target file context directly to conserve context size & tokens
            with open(app_file_path, "r", encoding="utf-8") as f:
                context = f.read()
            
            print("[2/5] Running test suite...")
            test_results = verifier.run_tests()
            
            if test_results["success"]:
                print(f"\n🎉 SUCCESS! All tests passed for {file_name}!")
                break
                
            print("[3/5] Tests failed. Packaging error logs for AI...")
            
            system_prompt = (
                "You are an autonomous AI coding agent. Review the provided code context "
                "and the failing test output. Find the bug. "
                "Reply with ONLY the complete, fixed Python code wrapped in a ```python ``` block. "
                "Do not include any explanations or conversational text."
            )
            
            user_prompt = (
                f"Target File: {file_name}\n\n"
                f"--- CODE CONTEXT ---\n{context}\n\n"
                f"--- TEST ERRORS ---\n{test_results['output']}\n\n"
                "Fix the bug in the target file and provide the updated code."
            )
            
            print("[4/5] Awaiting AI fix (with rate-limit safety)...")
            
            # Use safe wrapper instead of calling adapter directly
            ai_response = safe_generate_patch(adapter, system_prompt, user_prompt)
            
            if not ai_response:
                print("Skipping retry due to persistent API rate limits.")
                break

            print("[5/5] Extracting code and applying patch...")
            clean_code = CodeParser.extract_code(ai_response)
            
            if clean_code:
                FilePatcher.apply_patch(fixed_file_path, clean_code)
                print(f"✅ Patch applied! Saved to: {os.path.basename(fixed_file_path)}")
                break
            else:
                print("Failed to extract code from AI response. Retrying...\n")
                
            attempt += 1
            time.sleep(2)

        # Cool-down pause between processing different files
        print("⏸️ Pausing 3 seconds to avoid triggering API Rate Limits...")
        time.sleep(3)

if __name__ == "__main__":
    start_agent_loop()
