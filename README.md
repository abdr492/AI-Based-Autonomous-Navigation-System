# 🏎️ AI-Based Autonomous Navigation System

An end-to-end virtual simulation for an artificial intelligence-driven autonomous navigation platform. This project acts as an advanced sandbox replicating what large-scale AV companies (like Tesla, Waymo, or NVIDIA) deploy visually, without requiring expensive physical robotics or hardware components. 

The software includes a cohesive, photorealistic graphical simulation engine, automated A* route plotting, a mock-up of object detection frameworks, and a hyper-modern web-based telemetry dashboard.

---

## ✨ Features & Capabilities

- **Photorealistic Top-Down Simulation** (`virtual_simulation.py`)
  A robust `Pygame`-based environment rendering a detailed proving ground. Watch a dynamically pivoting EV calculate its path around procedurally modeled civilian traffic, pedestrians, and park trees. Features integrated GPS pathing lines and emergency active braking simulation.
- **YOLOv3 Object Detection Interface** (`step4_object_detection.py`)
  Full programmatic wrapper integrating Darknet YOLOv3-tiny through OpenCV's DNN module for real-time bounding boxes via simulated or direct camera feeds.
- **A* Spatial Path Planning**
  High-frequency evaluation matrix navigating the vehicle safely around unexpected dynamic obstacle interventions.
- **Hyperrealistic Web Dashboard** (`index.html`)
  A state-of-the-art telemetry interface boasting OLED aesthetic glassmorphism, completely animated concentric speed gauges, animated target reticles, and real-time JavaScript loops synthesizing live data from an AV engine.
- **Virtual HC-SR04 Sensor Logic** (`step5_obstacle_avoidance.py`)
  Pure software abstraction mimicking GPIO pins and hardware triggers to gauge "distances" and execute collision avoidance protocols instantly.

---

## 🛠️ Setup & Installation

All required external models and dependencies are managed automatically. 

1. **Prerequisites:** Python 3.x installed.
2. Ensure you are in the project root directory.
3. Simply execute the automation batch script:
```bash
run.bat
```
This single script will silently install library requirements (like `pygame`, `opencv-python`), launch the `index.html` dashboard, and simultaneously boot the `virtual_simulation.py` engine!

*(Alternatively, to run manually):*
* `pip install -r requirements.txt`
* `python setup_yolo.py` (Downloads the required YOLO weights & coco.names).
* `python virtual_simulation.py`

---

## 📂 Project Structure

- `virtual_simulation.py`: The crown jewel. Procedural rendering, collision logic, dynamic movement tracking, and A* algorithmic routing.
- `index.html`: The standalone web UI telemetry console.
- `step3_capture_video.py`: A simulated video feed or camera wrapper.
- `step4_object_detection.py`: Runs real-time YOLOv3 inference natively.
- `step5_obstacle_avoidance.py`: Demonstrates purely the virtual ultrasonic HC-SR04 logic and its programmatic outputs.
- `setup_yolo.py`: Python deployment script that securely downloads model binaries bypassing user-agent flags.
- `run.bat`: Simplified deployment runner.

---

## 🚦 Future Upgrades / Roadmap
- Expand the virtual engine to include multi-agent routing.
- Support Flask APIs to pipe *actual* Pygame coordinates back to the Web Dashboard.
- Train custom TensorFlow/PyTorch object sets explicitly on traffic signs.

***Designed for AI experimentation, algorithm visualization, and automated prototyping.***
