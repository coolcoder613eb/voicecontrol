# Voice-to-Keyboard Controller

## Prerequisites
- Vosk language model ([Download small English model](https://alphacephei.com/vosk/models))
- Microphone access

## Installation

1. **Install dependencies**:
```bash
pip install vosk pyaudio keyboard
```

2. **Non-Root Setup (Linux)**:
```bash
# Configure device permissions
sudo usermod -a -G tty,input $USER
sudo chmod +0666 /dev/uinput

# Create udev rules
echo 'KERNEL=="uinput", TAG+="uaccess"' | sudo tee /etc/udev/rules.d/50-uinput.rules
echo 'SUBSYSTEM=="input", MODE="0666" GROUP="plugdev"' | sudo tee /etc/udev/rules.d/12-input.rules
echo 'SUBSYSTEM=="misc", MODE="0666" GROUP="plugdev"' | sudo tee -a /etc/udev/rules.d/12-input.rules
echo 'SUBSYSTEM=="tty", MODE="0666" GROUP="plugdev"' | sudo tee -a /etc/udev/rules.d/12-input.rules

loginctl terminate-user $USER  # Relogin
```

3. **Download Vosk Model**

   Extract the model to a directory (default: `vosk-model-small-en-us-0.15`)

## Configuration
Create a `config.json` file with:
- `model_path`: Path to Vosk model directory
- `key_press_duration`: Global duration for press-and-release actions (seconds)
- `voice_commands`: Array of command objects with:
  - `text`: Voice command to recognize
  - `key`: Keyboard key to activate
  - `flags` (optional): Additional command parameters:
    - `action`: Key action (press/release/press_and_release, default: press_and_release)
    - `exclusive`: Release other keys first (true/false, default: false)
    - `duration`: Override global press duration (seconds)

Example config.json:
```json
{
    "model_path": "vosk-model-small-en-us-0.15",
    "key_press_duration": 0.2,
    "voice_commands": [
        {
            "text": "go",
            "key": "up",
            "flags": {
                "action": "press",
                "exclusive": true
            }
        },
        {
            "text": "no",
            "key": "any",
            "flags": {
                "action": "release"
            }
        },
        {
            "text": "bang",
            "key": "ctrl",
            "flags": {
                "duration": 0.5
            }
        }
    ]
}
```

## Usage
```bash
python main.py [--config path/to/config.json]
```

## Notes
1. Use standard key names from the [keyboard module documentation](https://github.com/boppreh/keyboard#key-names)
2. The `any` key in release commands will release all currently pressed keys
3. After configuring permissions on Linux, you should NOT need sudo to run the script
4. The Vosk model path in the script must match your download location
5. Exclusive commands release all pressed keys before executing
6. Command-specific durations override the global key_press_duration
