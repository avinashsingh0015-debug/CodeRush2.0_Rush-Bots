import os

class FilePatcher:
    @staticmethod
    def apply_patch(file_path: str, new_code: str) -> bool:
        """
        Writes the new, AI-generated code to the specified file.
        Creates the file automatically if it does not exist.
        """
        try:
            # 'w' mode will create the file if it isn't there!
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_code)
            return True
        except Exception as e:
            print(f"Failed to patch file: {str(e)}")
            return False