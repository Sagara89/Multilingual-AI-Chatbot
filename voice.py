import asyncio
import edge_tts
import pygame
import uuid
import speech_recognition as sr
import os
import time
import threading

# ---------------- INIT PYGAME ----------------
pygame.mixer.init()

# ---------------- LANGUAGE VOICES ----------------
VOICE_MAP = {
    "English": "en-US-GuyNeural",
    "Hindi": "hi-IN-MadhurNeural",
    "Kannada": "kn-IN-GaganNeural"
}

# ---------------- GLOBAL FLAG ----------------
is_speaking = False

# ---------------- GENERATE VOICE ----------------
async def generate_voice(text, voice, filename):

    communicate = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate="+20%"
    )

    await communicate.save(filename)

# ---------------- SPEAK ----------------
def speak(text, language="English"):

    global is_speaking

    filename = f"voice_{uuid.uuid4().hex}.mp3"

    voice = VOICE_MAP.get(
        language,
        "en-US-GuyNeural"
    )

    asyncio.run(
        generate_voice(text, voice, filename)
    )

    def play_audio():

        global is_speaking

        is_speaking = True

        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():

            if not is_speaking:
                pygame.mixer.music.stop()
                break

            time.sleep(0.1)

        pygame.mixer.music.stop()

        if os.path.exists(filename):
            os.remove(filename)

    threading.Thread(
        target=play_audio
    ).start()

# ---------------- STOP SPEAKING ----------------
def stop_speaking():

    global is_speaking

    is_speaking = False

    pygame.mixer.music.stop()

# ---------------- LISTEN ----------------
def listen():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        recognizer.adjust_for_ambient_noise(source)

        print("Listening...")

        try:
            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=8
            )

        except:
            return "No speech detected"

    try:
        text = recognizer.recognize_google(audio)
        return text

    except:
        return "Sorry, I didn't understand"