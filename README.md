# Voice-to-Keyboard Controller

## Prerequisites
- Vosk language model ([Download small English model](https://alphacephei.com/vosk/models))
- Microphone access
- Linux system with uinput support (for inputtino)

## Installation

1. **Install dependencies**:
```bash
pip install vosk pyaudio
```
2. **Install inputtino** (follow official [Python binding instructions](https://github.com/games-on-whales/inputtino/tree/stable/bindings/python#installation))

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

## Important Notes
1. After configuring permissions, you should NOT need sudo to run the script
2. The Vosk model path in the script must match your download location
3. New commands can be added by extending the `VOICE_COMMANDS` list
4. `press_and_release` delay (0.2s) can be adjusted in the code
