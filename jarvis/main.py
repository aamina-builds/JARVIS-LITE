"""
The glue: mic -> stt -> llm (with tools) -> tts -> speaker, on a loop.

Run with:  python -m jarvis.main
Press Ctrl+C, or say "stop listening", to quit.
"""

from jarvis.stt import listen_and_transcribe
from jarvis.llm import ask
from jarvis.tools import run_tool
from jarvis.tts import speak

EXIT_PHRASES = {"stop listening", "goodbye jarvis", "exit"}


def handle_turn(history: list[dict]) -> bool:
    """Runs one listen->think->speak cycle. Returns False to stop the loop."""
    user_text = listen_and_transcribe()
    if not user_text:
        return True

    print(f"You: {user_text}")
    if user_text.strip().lower() in EXIT_PHRASES:
        speak("Goodbye.")
        return False

    result = ask(user_text, history)

    if result["type"] == "tool_call":
        tool_result = run_tool(result["name"], result["arguments"])
        print(f"[tool] {result['name']} -> {tool_result}")
        reply = tool_result
    else:
        reply = result["content"]

    print(f"JARVIS: {reply}")
    speak(reply)

    history.append({"role": "user", "content": user_text})
    history.append({"role": "assistant", "content": reply})
    # Keep history short so the model stays fast and focused
    return True


def main():
    print("JARVIS is online. Speak after 'Listening...'. Say 'stop listening' to quit.")
    history: list[dict] = []
    try:
        while True:
            if not handle_turn(history):
                break
            history[:] = history[-10:]  # cap context length
    except KeyboardInterrupt:
        print("\nShutting down.")


if __name__ == "__main__":
    main()
