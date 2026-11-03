"""
Hands: real actions the assistant can take. Each tool is:
  1. a plain Python function
  2. a schema entry in TOOL_SCHEMAS describing it to the LLM

Add a new tool by writing a function + adding one schema entry below —
the model will decide on its own when to call it.
"""

import datetime
import webbrowser


def get_time() -> str:
    return datetime.datetime.now().strftime("It's %I:%M %p.")


def open_website(url: str) -> str:
    if not url.startswith("http"):
        url = "https://" + url
    webbrowser.open(url)
    return f"Opening {url}."


def open_app(app_name: str) -> str:
    # Minimal cross-platform example. Extend per-OS as needed
    # (subprocess.run(["open", "-a", app_name]) on macOS,
    #  subprocess.run([app_name]) on Linux/Windows, etc).
    import subprocess
    import sys

    try:
        if sys.platform == "darwin":
            subprocess.Popen(["open", "-a", app_name])
        elif sys.platform.startswith("linux"):
            subprocess.Popen([app_name])
        elif sys.platform == "win32":
            import os
            os.startfile(app_name)  # avoids shell=True, since app_name comes from the LLM
        return f"Opening {app_name}."
    except Exception:
        return f"I couldn't open {app_name} — is it installed?"


# Maps the name the LLM calls -> the actual Python function
TOOL_FUNCTIONS = {
    "get_time": lambda **kwargs: get_time(),
    "open_website": lambda **kwargs: open_website(kwargs.get("url", "")),
    "open_app": lambda **kwargs: open_app(kwargs.get("app_name", "")),
}

# Descriptions the LLM sees, in Ollama's tool-calling format
TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "Get the current local time.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "open_website",
            "description": "Open a website in the default browser.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "The URL to open"}
                },
                "required": ["url"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "open_app",
            "description": "Open a desktop application by name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "app_name": {"type": "string", "description": "Name of the app, e.g. 'Spotify'"}
                },
                "required": ["app_name"],
            },
        },
    },
]


def run_tool(name: str, arguments: dict) -> str:
    fn = TOOL_FUNCTIONS.get(name)
    if not fn:
        return f"Unknown tool: {name}"
    return fn(**arguments)
