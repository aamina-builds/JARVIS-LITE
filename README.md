# Jarvis Lite: Offline Voice Assistant

A voice assistant that runs **entirely on my own computer**: no paid APIs, no API keys, no cloud.
I speak, it listens, thinks, and answers out loud. It can also take real actions like opening websites and apps.

> **Demo:** *(add a screenshot, GIF or short video link here, this matters more than anything else in this README)*

## How it works

```
Microphone → Speech-to-Text → Local LLM (+ tools) → Text-to-Speech → Speakers
             faster-whisper      Ollama / Llama 3.1     Piper
```

| Stage | Tool | Role |
|---|---|---|
| Ears | `faster-whisper` | Transcribes mic audio locally |
| Brain | Ollama + Llama 3.1 | Understands the request and decides whether to call a tool |
| Voice | Piper TTS (`en_GB-alan-medium`) | Speaks the reply in a calm British voice |
| Hands | Python functions in `jarvis/tools.py` | Real actions the LLM can trigger (function calling) |
| Glue | `jarvis/main.py` | Runs the listen → think → speak loop and keeps short chat history |

## Features

- Fully offline and free: speech recognition, LLM and voice all run locally
- Tool use / function calling: tell the time, open a website, open a desktop app
- A JARVIS-style personality set through the system prompt (formal, dry wit, short replies)
- Conversation memory limited to the last 10 messages to keep responses fast
- Each module (`stt`, `llm`, `tts`) can be tested on its own
- Easy to extend: add a Python function plus one schema entry to give it a new skill

## Tech stack

Python 3.10+ · faster-whisper · Ollama (Llama 3.1) · Piper TTS · sounddevice · NumPy · Requests

## Setup

**1. Install dependencies**
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**2. Install Ollama and pull a model**: download from https://ollama.com, then:
```bash
ollama pull llama3.1
```

**3. Add a Piper voice**: download `en_GB-alan-medium.onnx` and its `.onnx.json` from
https://github.com/rhasspy/piper/releases and put both in the `voices/` folder.
(If you use another voice, update `VOICE_MODEL_PATH` in `jarvis/tts.py`.)

**4. Test each part separately**
```bash
python -m jarvis.stt
python -m jarvis.llm
python -m jarvis.tts
```

**5. Run it**
```bash
python -m jarvis.main
```
Speak when you see `Listening...` (it records 5 seconds per turn). Try *"What time is it?"* or *"Open YouTube"*.
Say **"stop listening"** or press `Ctrl+C` to quit.

## Adding your own tools

Open `jarvis/tools.py`, write a Python function, register it in `TOOL_FUNCTIONS`, and describe it in
`TOOL_SCHEMAS`. The LLM decides when to call it.

## Troubleshooting

- **Connection refused:** Ollama isn't running. Open the app or run `ollama serve`.
- **No audio input:** run `python -m jarvis.stt` alone and check your OS microphone permissions.
- **Robotic voice:** try a `-medium` or `-high` Piper voice.
- **Slow replies:** use a smaller model, e.g. `ollama pull llama3.2:3b`, and update `MODEL` in `jarvis/llm.py`.

## Known limitations & next steps

- Records a fixed 5 seconds per turn; a wake word ("Hey Jarvis") with `openWakeWord` would be a better experience
- `open_app` launches whatever app name the model returns; an allow-list of apps would make it safer
- Only three tools so far; ideas: calendar, smart-home control, web search
- A small on-screen interface (animated orb or waveform)

## What I learned

*(Write 3 to 4 honest sentences in your own words, for example what pipeline stages taught you, what was hardest, what you'd improve. Interviewers read this part.)*

## Credits

Built with help from Claude (Anthropic) as an AI coding assistant. Uses open-source projects: faster-whisper, Ollama, Piper and Llama 3.1.
Voice is a generic British voice model, not a clone of any real person or character.
