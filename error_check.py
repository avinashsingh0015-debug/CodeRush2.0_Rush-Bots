import os
import time
import shutil
from services.scanner import RepoScanner
from services.llm_adapter import LLMAdapter
from services.verifier import CodeVerifier
from services.parser import CodeParser
from services.patcher import FilePatcher

def safe_generate_patch(adapter, system_prompt, user_prompt, max_retries=5, initial_delay=5):
    delay = initial_delay
    for attempt in range(1, max_retries + 1):
        try:
            return adapter.generate_patch(system_prompt, user_prompt)
        except Exception as e:
            error_msg = str(e).lower()
            if "429" in error_msg or "rate limit" in error_msg or "resource_exhausted" in error_msg:
                print(f"⚠️ Rate limit hit (Attempt {attempt}/{max_retries}). Waiting {delay} seconds...")
                time.sleep(delay)
                delay *= 2
            else:
                raise e
    print("❌ Failed to get response from LLM after maximum retries.")
    return None

def run_ai_fixer(target_relative_path="app", max_attempts=3):
    logs = []
    def log(msg):
        print(msg)
        logs.append(msg)

    log("🚀 Starting CodeHarness V2 Multi-File Agent...\n")
    
    target_dir = os.path.dirname(os.path.abspath(__file__))
    app_dir = os.path.join(target_dir, "app")
    
    if not os.path.exists(app_dir):
        app_dir = target_dir

    # Fix 1: Filter ONLY target app files (Strictly ignore test_*, test*, and _fixed.py files)
    target_files = [
        f for f in os.listdir(app_dir) 
        if f.endswith(".py") 
        and not f.startswith("test") 
        and not f.endswith("_fixed.py")
    ]

    if not target_files:
        log("❌ No valid source target files found in 'app' directory.")
        return {"success": False, "logs": "\n".join(logs)}

    log(f"📋 Found {len(target_files)} source file(s) to process: {', '.join(target_files)}\n")

    adapter = LLMAdapter()
    verifier = CodeVerifier(target_directory=target_dir)

    all_passed = True

    for file_index, file_name in enumerate(target_files, 1):
        app_file_path = os.path.join(app_dir, file_name)
        backup_file_path = f"{app_file_path}.bak"
        
        # Original broken file safe backup
        shutil.copyfile(app_file_path, backup_file_path)
        
        log(f"==================================================")
        log(f"🎯 [{file_index}/{len(target_files)}] Processing Target File: {file_name}")
        log(f"==================================================")

        attempt = 1
        file_fixed = False

        try:
            while attempt <= max_attempts:
                log(f"\n--- ATTEMPT {attempt}/{max_attempts} for {file_name} ---")
                
                with open(app_file_path, "r", encoding="utf-8") as f:
                    target_code = f.read()
                
                # Associated unit test locate karein
                test_file_name = f"test_{file_name}"
                test_file_path = os.path.join(target_dir, "test", test_file_name)
                
                if os.path.exists(test_file_path):
                    with open(test_file_path, "r", encoding="utf-8") as f:
                        test_code = f.read()
                    context = f"--- TARGET FILE ({file_name}) ---\n{target_code}\n\n--- TEST FILE ---\n{test_code}"
                else:
                    context = f"--- TARGET FILE ({file_name}) ---\n{target_code}"

                # Target specific test execution
                test_results = verifier.run_tests(test_file_name=test_file_name if os.path.exists(test_file_path) else None)
                
                if test_results["success"]:
                    log(f"🎉 SUCCESS! All tests passed for {file_name}!")
                    file_fixed = True
                    break

                log("[3/5] Tests failed. Packaging error logs for AI...")
                system_prompt = (
                    "You are an autonomous AI coding agent. Review the provided code context "
                    "and the failing test output. Find the bug. "
                    "Reply with ONLY the complete, full Python code wrapped in a ```python ``` block. "
                    "Do not use ellipses (...), placeholders, or truncation. "
                    "Provide the entire file implementation from start to finish. "
                    "Do not include any explanations or conversational text."
                )
                
                user_prompt = (
                    f"--- CODE CONTEXT ---\n{context}\n\n"
                    f"--- TEST ERRORS ---\n{test_results['output']}\n\n"
                    "Fix the bug and provide the updated file."
                )

                log("[4/5] Awaiting AI fix (with rate-limit safety)...")
                ai_response = safe_generate_patch(adapter, system_prompt, user_prompt)

                if not ai_response:
                    log("Skipping retry due to persistent API rate limits.")
                    break

                log("[5/5] Extracting code and creating fixed file...")
                clean_code = CodeParser.extract_code(ai_response)

                if clean_code:
                    clean_code = "\n".join([line for line in clean_code.splitlines() if line.strip() != "..."])
                    
                    # 1. Permanent Corrected File Create Karein (_fixed.py)
                   # asd.py - Temp Verification Patch Update

                    # 1. Permanent Corrected File Create Karein (_fixed.py)
                    base, ext = os.path.splitext(app_file_path)
                    fixed_file_path = f"{base}_fixed{ext}"
                    FilePatcher.apply_patch(fixed_file_path, clean_code)

                    # 2. Verification ke liye both Original file path AND Fixed file path patch karein
                    FilePatcher.apply_patch(app_file_path, clean_code)

                    # Direct module reload force karein taaki pytest cache update ho jaye
                    test_file_name = f"test_{file_name}"
                    test_results = verifier.run_tests(test_file_name=test_file_name) 

                    # 2. Fix 2: Verification pass karwane ke liye original path par temporarily write karein
                    FilePatcher.apply_patch(app_file_path, clean_code)
                    log(f"✅ Corrected file created: {os.path.basename(fixed_file_path)}! Verifying...\n")
                else:
                    log("Failed to extract code from AI response. Retrying...\n")

                attempt += 1
                time.sleep(1)

        finally:
            # Re-verification poori hone ke baad original broken file restore ho jayegi
            if os.path.exists(backup_file_path):
                shutil.copyfile(backup_file_path, app_file_path)
                os.remove(backup_file_path)

        if not file_fixed:
            all_passed = False
            log(f"❌ Failed to resolve issues for {file_name}.\n")

        time.sleep(1)

    if all_passed:
        log("\n🎉 ALL SOURCE FILES SUCCESSFULLY FIXED AND CREATED!")
        return {"success": True, "logs": "\n".join(logs)}
    else:
        log("\n⚠️ Some files could not be fixed within max attempts.")
        return {"success": False, "logs": "\n".join(logs)}

if __name__ == "__main__":
    run_ai_fixer()
