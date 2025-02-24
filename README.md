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
- `key_press_duration`: Duration for press-and-release actions (seconds)
- `voice_commands`: Array of command objects with:
  - `text`: Voice command to recognize
  - `key`: Keyboard key to activate
  - `action`: Key action (press/release/press_and_release)

Example config.json:
```json
{
    "model_path": "vosk-model-small-en-us-0.15",
    "key_press_duration": 0.2,
    "voice_commands": [
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
        }
    ]
}
```

## Usage
```bash
python main.py [--config path/to/config.json]
```

## Notes
2. Use standard key names from the [keyboard module documentation](https://github.com/boppreh/keyboard#key-names)
3. The `any` key in release commands will release all currently pressed keys
1. After configuring permissions on Linux, you should NOT need sudo to run the script
2. The Vosk model path in the script must match your download location
