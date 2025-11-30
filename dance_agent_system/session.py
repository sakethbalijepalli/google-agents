import os
from typing import Optional

import os
from typing import Optional

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)

def _get_filepath(key):
    if not os.path.splitext(key)[1]:
        key += ".txt"
    return os.path.join(DATA_DIR, key)

def save_state(key, content):
    filepath = _get_filepath(key)
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Saved state to {filepath}"
    except Exception as e:
        return f"Failed to save state {key}: {e}"

def load_state(key):
    filepath = _get_filepath(key)
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception:
            return None
    return None

def get_context(keys):
    context_parts = []
    for key in keys:
        content = load_state(key)
        if content:
            context_parts.append(f"--- {key} ---\n{content}\n")
        else:
            context_parts.append(f"--- {key} ---\n(No data found)\n")
    
    return "\n".join(context_parts)
