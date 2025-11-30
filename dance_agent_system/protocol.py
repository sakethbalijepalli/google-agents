import json
from typing import Any, Dict, Optional

def format_message(sender: str, receiver: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> str:
    """Creates a formatted AgentMessage JSON string."""
    msg = {
        "sender": sender,
        "receiver": receiver,
        "content": content,
        "metadata": metadata
    }
    return json.dumps(msg, indent=2)

def compact_context(text: str, max_length: int = 5000) -> str:
    """Compacts context by truncating it if it exceeds max_length."""
    if not text or len(text) <= max_length:
        return text
    
    return text[:max_length] + f"\n\n[...Truncated {len(text) - max_length} chars...]"
