✋ Virtual Keyboard with Hand Gesture Control

A Python-powered virtual keyboard that lets you type using hand gestures — no physical keyboard needed!  
It works by tracking your index and middle fingers and measuring the distance between them to detect key presses.  
Perfect for touchless typing, accessibility, and creative experiments.

🚀 Features
- Touchless Typing — Type without touching any physical device.
- Distance-Based Gesture Detection — Key press happens when the gap between your index & middle fingers is below a set threshold.
- Real-Time Computer Vision — Uses OpenCV and MediaPipe for accurate hand tracking.
- Customizable Layout — Change keys, sizes, and gesture sensitivity.
- Accessible Input Method — Useful for hands-free operation.

🛠️ Tech Stack
- Python
- OpenCV – Video capture & image processing
- MediaPipe – Hand tracking & landmark detection
- PyAutoGUI – Simulating keystrokes
  
📸 How It Works
1. Start the program — Webcam opens and tracks your hand.
2. Move fingers to a key — Hover index finger over the key area.
3. Pinch Gesture — Bring index and middle fingers close together.
4. Key Press Triggered — Distance threshold crossed → key is typed.
