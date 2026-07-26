import sys
import os
import uuid

import pyaudiowpatch as pyaudio
sys.modules["pyaudio"] = pyaudio  # alias so speech_recognition finds it

import speech_recognition as sr
from gtts import gTTS


LANGUAGE_CODES = {
    "English": {"stt": "en-US", "tts": "en"},
    "Sinhala": {"stt": "si-LK", "tts": "si"}
}


def listen_voice(language="English"):
    """
    Records from the microphone and returns recognized text,
    or None if nothing could be recognized.
    """
    stt_lang = LANGUAGE_CODES.get(language, LANGUAGE_CODES["English"])["stt"]
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source, timeout=5, phrase_time_limit=20)
        return r.recognize_google(audio, language=stt_lang)
    except sr.WaitTimeoutError:
        print("Voice: no speech detected in time.")
        return None
    except sr.UnknownValueError:
        print("Voice: could not understand audio.")
        return None
    except Exception as e:
        print(f"Voice recognition failed: {e}")
        return None


def speak_text(text, language="English"):
    """
    Converts text to speech (mp3) and returns the file path,
    or None if it failed.
    """
    tts_lang = LANGUAGE_CODES.get(language, LANGUAGE_CODES["English"])["tts"]
    try:
        os.makedirs("data/audio", exist_ok=True)
        filename = f"data/audio/{uuid.uuid4().hex}.mp3"
        gTTS(text=text, lang=tts_lang).save(filename)
        return filename
    except Exception as e:
        print(f"Text-to-speech failed: {e}")
        return None