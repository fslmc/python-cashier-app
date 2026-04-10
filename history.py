import os
from pathlib import Path
import subprocess
import platform

def collect_all_receipt():
    try:
        history_dir = Path("./history")

        if not history_dir.exists():
            history_dir.mkdir(parents=True)
            return [], None
        
        receipts = sorted(
            list(Path("./history").glob("*.pdf")),
            key=os.path.getmtime,
            reverse=True
        )

        return receipts, None
    except Exception as e:
        print(f"⚠️ Error accessing history folder: {e}")
        return []

def open_receipt(filepath):
    """
    Opens the receipt file using the system's default PDF viewer.
    """
    path = Path(filepath)
    
    if not path.exists():
        return False, FileNotFoundError(f"Receipt {path.name} was not found.")

    # Cross-platform file opening logic
    current_os = platform.system()
    try:
        if current_os == "Windows":
            os.startfile(path)
        elif current_os == "Darwin":  # macOS
            subprocess.run(["open", str(path)])
        else:  # Linux
            subprocess.run(["xdg-open", str(path)])
        return True, None
    except Exception as e:
        return False, e


if __name__ == "__main__" :
    print(collect_all_receipt())