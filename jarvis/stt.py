"""
Ears: records a few seconds of mic audio and transcribes it to text, locally,
using faster-whisper (a fast reimplementation of OpenAI's Whisper).

No cloud calls, no API key, runs on CPU (slower) or GPU (fast) fine.
"""

import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel

SAMPLE_RATE = 16000
RECORD_SECONDS = 5

# "base" is a good speed/accuracy tradeoff for a starter project.
# Options (fastest -> most accurate): tiny, base, small, medium, large-v3
_model = WhisperModel("base", device="cpu", compute_type="int8")


def record_audio(seconds: int = RECORD_SECONDS) -> np.ndarray:
    """Records `seconds` of mono mic audio and returns it as a float32 array."""
    print("Listening...")
    audio = sd.rec(
        int(seconds * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32",
    )
    sd.wait()
    return audio.flatten()


def transcribe(audio: np.ndarray) -> str:
    """Runs Whisper on the given audio array and returns the transcribed text."""
    segments, _info = _model.transcribe(audio, language="en")
    return " ".join(segment.text.strip() for segment in segments).strip()


def listen_and_transcribe(seconds: int = RECORD_SECONDS) -> str:
    audio = record_audio(seconds)
    return transcribe(audio)


# --- Notes on upgrading this file ---
# To add a wake word ("Hey Jarvis") instead of always recording on Enter:
#   pip install openwakeword
# Then run a small always-on loop that listens for the wake word and only
# calls listen_and_transcribe() once it fires.


if __name__ == "__main__":
    text = listen_and_transcribe()
    print(f"You said: {text!r}")
