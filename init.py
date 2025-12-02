# Different from __init__.py to avoid circular import issues

import os

def init_venv():
    activate_path = "p2p_venv/bin/activate"
    resp = os.system(f"source {activate_path}")

if __name__ == "__main__":
    init_venv()