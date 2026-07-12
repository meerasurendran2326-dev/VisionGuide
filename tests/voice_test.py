import pyttsx3

engine = pyttsx3.init()

engine.setProperty("rate", 150)
engine.setProperty("volume", 1.0)

voices = engine.getProperty("voices")

# Female voice (Windows Zira if available)
for voice in voices:
    if "zira" in voice.name.lower():
        engine.setProperty("voice", voice.id)
        break


def speak(text):
    print("Speaking:", text)
    engine.stop()
    engine.say(text)
    engine.runAndWait()


print("Voice Test Started\n")

speak("Hello. Welcome to Vision Guide.")
speak("Person ahead.")
speak("Chair on your left.")
speak("Bus on your right.")
speak("Traffic light is red. Please wait.")
speak("Traffic light is green. You can cross.")
speak("Room number two zero five detected.")
speak("Thank you.")