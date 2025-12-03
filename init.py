# Different from __init__.py to avoid circular import issues
# This file is to initialize virtual environment
import os

# Function to initialize virtual environment
def init_venv():
    if os.name == "posix":
        print("Activate the venv in your current shell with:")
        print("\n  'source p2p_venv/bin/activate'\n")
        print("or run scripts directly with:")
        print("\n  'p2p_venv/bin/python your_script.py'")
    elif os.name == "nt":
        print(r"Run: p2p_venv\\Scripts\\activate.bat (Windows cmd) or use the appropriate PowerShell activation)")

if __name__ == "__main__":
    print("DEV OS: ", os.name)
    init_venv()