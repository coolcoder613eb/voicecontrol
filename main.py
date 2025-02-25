import json
import argparse
import time
import vosk
import pyaudio
import keyboard

pressed_keys = []


def process_text(text, voice_commands, key_press_duration):
    global pressed_keys
    for word_unfiltered in text.split():
        word = "".join(filter(str.isalpha, word_unfiltered.strip().lower()))
        print("Word:", word)
        for command in voice_commands:
            if command["text"].lower() == word:
                key_str = command["key"]
                flags = command.get("flags", {})
                action = flags.get("action", "press_and_release")
                exclusive = flags.get("exclusive", False)
                duration = flags.get("duration", key_press_duration)

                # Handle exclusive flag
                if exclusive and action in ["press", "press_and_release"]:
                    print("Exclusive: Releasing all keys before pressing")
                    for key in pressed_keys.copy():
                        keyboard.release(key)
                        pressed_keys.remove(key)

                if key_str == "any" and action == "release":
                    print("Releasing all keys")
                    for key in pressed_keys.copy():
                        keyboard.release(key)
                        pressed_keys.remove(key)
                    return

                print(f"Action: {action} {key_str}")

                if action == "press_and_release":
                    keyboard.press(key_str)
                    time.sleep(duration)
                    keyboard.release(key_str)
                elif action == "press":
                    keyboard.press(key_str)
                    pressed_keys.append(key_str)
                elif action == "release":
                    keyboard.release(key_str)
                    if key_str in pressed_keys:
                        pressed_keys.remove(key_str)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config", default="config.json", help="Path to configuration file"
    )
    args = parser.parse_args()

    # Load configuration
    with open(args.config) as f:
        config = json.load(f)

    model_path = config.get("model_path", "vosk-model-small-en-us-0.15")
    voice_commands = config.get("voice_commands", [])
    key_press_duration = config.get("key_press_duration", 0.2)

    print("Initializing speech recognition...")
    model = vosk.Model(model_path)
    text_elements = [cmd["text"] for cmd in voice_commands] + ["[unk]"]
    recognizer = vosk.KaldiRecognizer(model, 16000, json.dumps(text_elements))

    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=1024,
    )

    print("Speak now...")
    prev_partial = ""
    try:
        while True:
            data = stream.read(1024)
            if len(data) == 0:
                break

            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "")
                if text and text == prev_partial:
                    prev_partial = ""
            else:
                partial = json.loads(recognizer.PartialResult())
                text = partial.get("partial", "")
                if text and text != prev_partial:
                    process_text(text, voice_commands, key_press_duration)
                    prev_partial = text

    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        # Release all pressed keys
        for key in pressed_keys.copy():
            keyboard.release(key)
            pressed_keys.remove(key)
