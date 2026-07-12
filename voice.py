import pyttsx3
import time
import threading
# ----------------------------------------
# Initialize Engine
# ----------------------------------------
engine = pyttsx3.init()

engine.setProperty("rate", 150)
engine.setProperty("volume", 1.0)

# ----------------------------------------
# Select Female Voice (if available)
# ----------------------------------------
voices = engine.getProperty("voices")

female_voice = None

for voice in voices:

    name = voice.name.lower()

    if "zira" in name or "female" in name:
        female_voice = voice.id
        break

if female_voice:
    engine.setProperty("voice", female_voice)

# ----------------------------------------
# Voice Cooldown
# ----------------------------------------
_last_message = ""
_last_time = 0
VOICE_DELAY = 4   # seconds
_voice_lock = threading.Lock()
# ----------------------------------------
# Speak Function
# ----------------------------------------
def speak(text):

    global _last_message, _last_time


    if not text:
        return


    current_time = time.time()


    # Prevent repeated message

    if (
        text == _last_message
        and current_time - _last_time < VOICE_DELAY
    ):
        return



    try:

        with _voice_lock:

            print("🔊", text)


            engine.stop()


            engine.say(text)

            engine.runAndWait()



        _last_message = text

        _last_time = current_time



    except Exception as e:

        print(
            "Voice Error:",
            e
        )