# 🧙‍♂️ Wizard War

A gesture-controlled multiplayer fighting game built with Godot Engine and Python. Control your wizard characters using hand gestures detected through your webcam!

## 🎥 Demo

> A quick look at **Wizard War** in action — gesture-controlled combat in real time.
<p align="center">
  <img src="demo/wizard_war_demo.gif" width="600">
</p>
*Live hand-gesture control using MediaPipe + Godot (no keyboard input).*


## ✨ Features

- **Gesture-Based Controls**: Use hand gestures captured by webcam to control game characters
- **Real-time Hand Tracking**: Powered by MediaPipe for accurate hand landmark detection
- **Two Player Support**: Simultaneous control with left hand (Player 1) and right hand (Player 2)
- **UDP Communication**: Low-latency gesture-to-game communication via UDP sockets

## 🎮 Gesture Controls

### Hand Gestures
| Gesture | Action |
|---------|--------|
| **Fist** (0 fingers) | Attack 1 |
| **Peace Sign** (Index + Middle) | Jump |
| **Open Palm** (4+ fingers) | Attack 2 |
| **Index Pointing Left** | Move Left |
| **Index Pointing Right** | Move Right |

### Player Assignment
- **Left Hand** → Player 1 (Port 9000)
- **Right Hand** → Player 2 (Port 9001)

## 🛠️ Technologies Used

- **Godot Engine** - Game engine for rendering and game logic
- **Python 3.11** - Backend for gesture recognition
- **MediaPipe** - Hand tracking and landmark detection
- **OpenCV** - Camera input and image processing
- **Socket (UDP)** - Real-time communication between Python and Godot

## 📋 Requirements

- Python 3.11
- Webcam
- Windows OS (tested on Windows)

### Python Dependencies
- opencv-python (cv2)
- mediapipe
- numpy

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/tanujbishtt/Wizard_War.git
   cd Wizard_War
   ```

2. **Activate the virtual environment(use py 3.11)[Optional]**
   ```bash
   # Windows
   .\Scripts\Activate.ps1
   ```

3. **Install dependencies** (if needed)
   ```bash
   pip install opencv-python mediapipe numpy
   ```

## 🎯 How to Run

### Step 1: Start the Gesture Controller
Run the Python gesture recognition script:
```bash
python Include/main.py
```

This will:
- Open your webcam
- Display a window showing detected hand landmarks
- Start listening for gestures on both hands
- Send gesture commands via UDP to ports 9000 (P1) and 9001 (P2)

### Step 2: Launch the Game
1. Open the Godot project located in `godot_project/`
2. Run the project (F5 or click Play button)
3. The game will receive gesture commands and control the wizard characters

### Controls
- Position your hands in front of the webcam
- Make gestures with your left hand to control Player 1
- Make gestures with your right hand to control Player 2
- Press **ESC** in the gesture controller window to quit

## 📁 Project Structure

```
Wizard_War/
├── Include/
│   ├── main.py              # Main gesture recognition script
│   ├── GestureWizardPvP.cpp # C++ components
│   └── icon files
├── godot_project/
│   ├── assets/              # Game sprites and images
│   │   ├── Player_01/       # Wizard 1 animations
│   │   ├── Player_02/       # Wizard 2 animations
│   │   └── background/      # Background frames
│   ├── scenes/              # Godot scene files
│   │   ├── main.tscn        # Main game scene
│   │   ├── main_menu.tscn   # Menu scene
│   │   ├── player_01.tscn   # Player 1 character
│   │   └── player_02.tscn   # Player 2 character
│   └── project.godot        # Godot project file
└── README.md
```

## ⚙️ Configuration

Edit `Include/main.py` to modify:
- **UDP Ports**: Change `UDP_PORT_P1` and `UDP_PORT_P2`
- **Debounce Frames**: Adjust `DEBOUNCE_FRAMES` for gesture stability
- **Detection Confidence**: Modify `min_detection_confidence` and `min_tracking_confidence`

## 🐛 Troubleshooting

**Webcam not detected**
- Ensure no other application is using the webcam
- Try changing camera index in `cv2.VideoCapture(0)` to `1` or `2`

**Gestures not recognized**
- Ensure good lighting conditions
- Keep hands clearly visible to the camera
- Adjust detection confidence thresholds

**Game not receiving commands**
- Verify UDP ports match between Python script and Godot game
- Check firewall settings allow UDP communication on ports 9000 and 9001

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## 📄 License

This project is open source and available for educational purposes.

## 👨‍💻 Author

Created with ❤️ by Me :>

---

**Have fun controlling wizards with your hands! 🧙‍♂️✨**
