"""Voice command recognition for VisionGuide AI.

This module listens for spoken commands from the default microphone and
returns recognized text in lowercase English.
"""

import speech_recognition as sr


def listen_command():
    """
    Listen for a voice command using the default microphone.

    The recognizer listens for up to 5 seconds and attempts to transcribe
    the speech using Google Speech Recognition. If recognition fails or the
    microphone is unavailable, the function returns None.

    Returns:
        str | None: The recognized command as lowercase text, or None if no
        command could be understood.
    """
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

        try:
            command = recognizer.recognize_google(audio, language="en-US")
            return command.lower().strip() if command else None

        except sr.UnknownValueError:
            return None

        except sr.RequestError:
            return None

        except sr.WaitTimeoutError:
            return None

    except sr.WaitTimeoutError:
        return None

    except sr.UnknownValueError:
        return None

    except OSError:
        return None

    except Exception:
        return None
