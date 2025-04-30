import os
import json

STATE_FILE = "transcribe_state.json"

def save_state(file_path: str, model: str, language: str):
    state = {
        "file": file_path,
        "model": model,
        "language": language
    }
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f)

def load_state():
    if not os.path.exists(STATE_FILE):
        return None
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

def clear_state():
    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)