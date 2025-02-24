import json
import vosk
import pyaudio
from inputtino import Keyboard, KeyCode
import time

# Configuration of voice commands and their corresponding key actions
VOICE_COMMANDS = [
    {
        "text": "go",
        "key": "up",
        "action": "press"
    },
    {
        "text": "no",
        "key": "any",
        "action": "release"
    },
    {
        "text": "right",
        "key": "right",
        "action": "press"
    },
    {
        "text": "left",
        "key": "left",
        "action": "press"
    },
    {
        "text": "open",
        "key": "space",
        "action": "press_and_release"
    },
    {
        "text": "back",
        "key": "down",
        "action": "press"
    },
    {
        "text": "bang",
        "key": "ctrl",
        "action": "press_and_release"
    },
]

pressed_keys = []

def process_text(text):
    global pressed_keys
    for word_unfiltered in text.split():
        word = ''.join(filter(str.isalpha, word_unfiltered.strip().lower()))
        print("Word:", word)
        for command in VOICE_COMMANDS:
            if command["text"].lower() == word:
                action = command["action"]
                if command["key"] == "any" and action == "release":
                    print("Releasing all keys")
                    while pressed_keys:
                        keyboard.release(pressed_keys.pop())
                else:
                    key = KeyCode.from_str(command["key"])

                    print(f"Action: {action} {key}")

                    if action == "press_and_release":
                        keyboard.press(key)
                        time.sleep(0.2)  # Short press duration
                        keyboard.release(key)
                    elif action == "press":
                        keyboard.press(key)
                        pressed_keys.append(key)
                    elif action == "release":
                        keyboard.release(key)
                        if key in pressed_keys:
                            pressed_keys.remove(key)

if __name__ == "__main__":
    keyboard = Keyboard()
    print("Initializing speech recognition...")

    # Initialize Vosk model (download from https://alphacephei.com/vosk/models)
    model_path = "vosk-model-small-en-us-0.15"  # Path to your Vosk model directory
    model = vosk.Model(model_path)
    text_elements = [command["text"] for command in VOICE_COMMANDS]
    text_elements.append("[unk]")
    recognizer = vosk.KaldiRecognizer(model, 16000, json.dumps(text_elements))

    # Initialize audio input
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=1024)

    print("Speak now...")
    prev_partial = ""
    try:
        while True:
            data = stream.read(1024)
            if len(data) == 0:
                break

            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get('text', '')
                if text and text == prev_partial:
                    prev_partial = ""
            else:
                partial = json.loads(recognizer.PartialResult())
                text = partial.get('partial', '')
                if text and text != prev_partial:
                    process_text(text)
                    prev_partial = text

    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        # Release all pressed keys on exit
        while pressed_keys:
            key = pressed_keys.pop()
            keyboard.release(key)
