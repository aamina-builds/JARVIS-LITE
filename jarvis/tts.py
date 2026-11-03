"""
Voice: converts text to speech and plays it, using Piper (local, free TTS).

Setup: download a voice .onnx + .onnx.json pair from
https://github.com/rhasspy/piper/releases into a `voices/` folder,
then point VOICE_MODEL_PATH at it.

Using "en_GB-alan-medium" here — a formal, measured British male voice.
It's the closest free/legal match to a JARVIS-style tone (calm, precise,
faintly clipped) without cloning anyone's actual voice. Swap the filename
for any other Piper voice if you prefer a different accent/gender.
"""

import subprocess
import sys

import sounddevice as sd
import numpy as np

VOICE_MODEL_PATH = "voices/en_GB-alan-medium.onnx"  # <- update this path


def speak(text: str) -> None:
    """Runs Piper on `text` and plays the resulting audio through the speakers."""
    if not text:
        return

    result = subprocess.run(
        [
            "piper",
            "--model", VOICE_MODEL_PATH,
            "--output-raw",
        ],
        input=text.encode("utf-8"),
        capture_output=True,
    )

    if result.returncode != 0:
        print(f"[tts error] {result.stderr.decode(errors='ignore')}", file=sys.stderr)
        print(f"[fallback, printing instead]: {text}")
        return

    audio = np.frombuffer(result.stdout, dtype=np.int16)
    sd.play(audio, samplerate=22050)
    sd.wait()


if __name__ == "__main__":
    speak("Hello. This is a test of your local voice assistant.")
