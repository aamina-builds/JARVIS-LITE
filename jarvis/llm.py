"""
Brain: sends text to a local LLM (via Ollama) and gets back either a normal
reply, or a "tool call" telling us to run one of the functions in tools.py.

Ollama must be installed and running (it starts automatically after install,
or run `ollama serve` manually). Docs: https://ollama.com
"""

import json
import requests

from jarvis.tools import TOOL_SCHEMAS

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.1"  # swap for "llama3.2:3b" if you want faster/lighter

SYSTEM_PROMPT = (
    "You are JARVIS, a highly capable personal assistant in the style of a "
    "formal, unflappable British household AI. Address the user as 'sir' or "
    "'ma'am' occasionally (not every line). Speak with dry, understated wit "
    "and precise, economical phrasing — never gushing or overly enthusiastic. "
    "Stay calm and composed even when the request is trivial or the user is "
    "flustered. Keep spoken replies short (1-3 sentences) since they'll be "
    "read aloud. Use a tool whenever one clearly fits the request instead of "
    "guessing the answer yourself."
)


def ask(user_text: str, history: list[dict] | None = None) -> dict:
    """
    Sends the user's text (plus optional prior turns) to the local model.
    Returns a dict: {"type": "text", "content": str}
                 or {"type": "tool_call", "name": str, "arguments": dict}
    """
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": user_text})

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "messages": messages,
            "tools": TOOL_SCHEMAS,
            "stream": False,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    message = data["message"]

    tool_calls = message.get("tool_calls")
    if tool_calls:
        call = tool_calls[0]["function"]
        return {
            "type": "tool_call",
            "name": call["name"],
            "arguments": call.get("arguments", {}),
        }

    return {"type": "text", "content": message.get("content", "")}


if __name__ == "__main__":
    result = ask("What time is it right now?")
    print(json.dumps(result, indent=2))
