# 🏎️ AI-Based Autonomous Navigation System

An end-to-end virtual simulation for an artificial intelligence-driven autonomous navigation platform. This project acts as an advanced sandbox replicating what large-scale AV companies (like Tesla, Waymo, or NVIDIA) deploy visually, without requiring expensive physical robotics or hardware components. 

The software includes a cohesive, photorealistic graphical simulation engine, automated A* route plotting, a mock-up of object detection frameworks, and a hyper-modern web-based telemetry dashboard.

---

## ✨ Features & Capabilities

### Core Simulation Engine
- **Multi-Agent Autonomous Navigation** (`virtual_simulation.py`)
  - Pygame-based 25x25 grid environment with procedural obstacle generation
  - 3 autonomous agents (Blue, Purple, Orange) running simultaneously
  - Real-time collision detection and avoidance
  - Dynamic pathfinding with continuous rerouting

- **Advanced A* Path Planning Algorithm**
  - High-frequency path recalculation around obstacles
  - Optimized neighbor discovery for efficient traversal
  - Heuristic-based route optimization
  - Real-time path visualization with colored overlays

### Intelligent Obstacle Management
- **Static Obstacles**: Trees, traffic cones, parked cars, pedestrians
- **Dynamic Obstacles**: Real-time pedestrian detection and emergency braking
- **Collision Avoidance**: Multi-agent traffic yielding logic with status updates
- **Procedural Generation**: Randomized 15% grid obstacle density for realistic environments

### Real-Time Telemetry System
- **Flask Backend** (`app.py`)
  - RESTful API endpoints for telemetry data updates
  - `/update_telemetry` - Receive live sensor data
  - `/get_telemetry` - Retrieve current system state
  - Threaded telemetry broadcast (10Hz update rate)

- **Interactive Web Dashboard** (`index.html`)
  - OLED glassmorphism design aesthetic
  - Animated concentric speed gauge (0-100 KM/H)
  - Real-time sensor data display:
    - Front clearance distance
    - Lane deviation tracking
    - Object density counter
    - Network latency monitoring
  - Live A* path planning logs (10 most recent entries)
  - Live vision feed coordinates and FPS counter
  - Status indicator with color-coded alerts (Green/Yellow/Red)

### System Reliability
- **Auto-Restart Launcher** (`launcher.py`)
  - Continuous simulation management
  - Automatic restart on exit
  - Graceful shutdown handling
  - Real-time status logging

### Detection & Awareness
- **YOLOv3 Object Detection Interface** (`step4_object_detection.py`)
  - Darknet YOLOv3-tiny integration via OpenCV DNN
  - Real-time bounding box generation
  - Class confidence scoring
  - Simulated and live camera feed support

- **Virtual HC-SR04 Ultrasonic Sensor** (`step5_obstacle_avoidance.py`)
  - Software-abstracted distance measurement
  - Collision alert thresholds
  - Emergency braking protocols
  - Range-based obstacle classification

### Real-Time Monitoring
- **Status Broadcasting**
  - AUTOPILOT ENGAGED (normal cruising)
  - EMERGENCY BRAKE / YIELDING (obstacle detected)
  - DYNAMIC ALERT! PEDESTRIAN (emergency stop)
  - Destination Reached! (navigation complete)

- **Live Data Metrics**
  - Current speed and target speed
  - Front clearance and lane deviation
  - Detected object count
  - Network ping and FPS
  - Agent coordinates and direction vectors

---

## 🛠️ Setup & Installation

### Quick Start

1. **Prerequisites:** Python 3.8+ installed on your system

2. **Clone the Repository:**
```bash
git clone https://github.com/abdr492/AI-Based-Autonomous-Navigation-System.git
cd AI-Based-Autonomous-Navigation-System
```

3. **Install Dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run the System:**
```bash
# Option 1: Using the auto-restart launcher (Recommended)
python launcher.py

# Option 2: Run components separately
# Terminal 1 - Start Flask Dashboard
python app.py

# Terminal 2 - Start Virtual Simulation
python virtual_simulation.py
```

5. **Access the Dashboard:**
Open your browser and navigate to:
```
http://127.0.0.1:5000/
```

### Optional Setup
- Run YOLO setup script to download model weights: `python setup_yolo.py`
- Custom object detection: `python step4_object_detection.py`
- Video capture simulation: `python step3_capture_video.py`

---

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────┐
│         Multi-Agent Autonomous Navigation System         │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
   ┌────▼─────┐      ┌─────▼──────┐     ┌─────▼─────┐
   │  Agent   │      │   Agent    │     │   Agent   │
   │  (Blue)  │      │ (Purple)   │     │ (Orange)  │
   └────┬─────┘      └─────┬──────┘     └─────┬─────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                  ┌─────────▼──────────┐
                  │  Pygame Engine     │
                  │ (Simulation Loop)  │
                  └─────────┬──────────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
         ┌────▼─────┐  ┌───▼────┐  ┌───▼─────┐
         │ A* Path  │  │ Collision  │ Obstacle │
         │ Planning │  │ Detection  │ Detection│
         └────┬─────┘  └───┬────┘  └───┬─────┘
              │             │             │
              └─────────────┼─────────────┘
                            │
                  ┌─────────▼──────────┐
                  │  Telemetry Thread  │
                  │ (HTTP POST 10Hz)   │
                  └─────────┬──────────┘
                            │
                  ┌─────────▼──────────┐
                  │   Flask Backend    │
                  │   (port 5000)      │
                  └─────────┬──────────┘
                            │
                  ┌─────────▼──────────┐
                  │ Web Dashboard UI   │
                  │   (JavaScript)     │
                  └────────────────────┘
```

---

## 📂 Project Structure

```
AI-Based-Autonomous-Navigation-System/
├── app.py                          # Flask backend (port 5000)
├── virtual_simulation.py            # Main Pygame simulation engine
├── launcher.py                      # Auto-restart launcher
├── index.html                       # Web dashboard UI
├── requirements.txt                 # Python dependencies
├── setup_yolo.py                    # YOLO model downloader
├── step3_capture_video.py           # Video feed simulator
├── step4_object_detection.py        # YOLOv3 detection interface
├── step5_obstacle_avoidance.py      # HC-SR04 sensor simulation
├── train_traffic_signs.py           # Custom training script
├── yolov3-tiny.cfg                  # YOLO config file
├── coco.names                       # COCO dataset class labels
├── .gitignore                       # Git exclusions
├── README.md                        # This file
└── images/                          # Documentation images
    ├── Virtual-Simulation.png
    ├── dashbaord_1.png
    └── code.png
```

---

## 🚀 API Endpoints

### Telemetry Update
**POST** `/update_telemetry`
```json
{
  "sys_status": "AUTOPILOT ENGAGED",
  "status_color": "var(--accent-green)",
  "speed": 42.5,
  "distance": 145,
  "fps": 15,
  "ping": 14,
  "logs": ["[Agent-Blue] Path calculated", "..."],
  "tracker_coords": "X:342 Y:128",
  "obj_count": 6
}
```

### Get Current Telemetry
**GET** `/get_telemetry`
```json
{
  "sys_status": "AUTOPILOT ENGAGED",
  "status_color": "var(--accent-green)",
  "speed": 42.5,
  "distance": 145,
  "fps": 15,
  "ping": 14,
  "logs": ["..."],
  "tracker_coords": "X:342 Y:128",
  "obj_count": 6
}
```

---

## 🚦 Roadmap & Future Upgrades

### Phase 1 (Current)
- ✅ Multi-agent autonomous navigation simulation
- ✅ Real-time Flask telemetry backend
- ✅ Interactive web dashboard with live metrics
- ✅ A* pathfinding with dynamic rerouting
- ✅ Collision detection and avoidance
- ✅ Emergency braking system

### Phase 2 (Planned)
- 🔄 Integration with physical robot hardware (ROS support)
- 🔄 Custom neural network training for traffic signs
- 🔄 LIDAR simulation with point cloud rendering
- 🔄 Multi-threaded sensor fusion pipeline
- 🔄 Docker containerization for deployment

### Phase 3 (Experimental)
- 📡 GPS waypoint navigation system
- 📡 Lane detection with OpenCV
- 📡 Deep reinforcement learning for adaptive navigation
- 📡 WebSocket real-time communication
- 📡 Multi-vehicle coordination protocols

---

## 📈 Performance Metrics

| Component | Specification |
|-----------|---------------|
| Simulation FPS | 15 Hz |
| Telemetry Update Rate | 10 Hz |
| Pathfinding Algorithm | A* with heuristic |
| Grid Resolution | 25x25 cells |
| Max Agents | 3 (scalable) |
| Detection Model | YOLOv3-tiny |
| Framework | Pygame + Flask |
| Dashboard Refresh | 1000ms intervals |
| Latency | 10-20ms average |

---

## 🛡️ Safety Features

- **Emergency Braking**: Automatic stop on pedestrian detection
- **Collision Avoidance**: Multi-agent traffic management
- **Continuous Monitoring**: 10Hz telemetry updates
- **Status Alerts**: Real-time visual feedback (Red/Yellow/Green)
- **Path Validation**: Obstacle detection before movement
- **Dynamic Rerouting**: Instant pathfinding recalculation

---

## 🔧 Configuration

### Simulation Parameters
Edit `virtual_simulation.py` to modify:
```python
WIDTH, HEIGHT = 600, 600       # Window dimensions
ROWS = 25                      # Grid size (25x25)
FPS = 15                       # Simulation frequency
GRID_SIZE = WIDTH // ROWS      # Cell size (24 pixels)
```

### Telemetry Settings
Edit `app.py` to modify:
```python
app.run(port=5000, debug=False, threaded=True)
```

### Dashboard Styling
Edit `index.html` CSS variables:
```css
--accent-green: #2ecc71;
--accent-red: #e74c3c;
--accent-yellow: #f39c12;
```

---

## 📚 Key Technologies

- **Pygame**: Graphics rendering and simulation loop
- **Flask**: Web framework for telemetry API
- **OpenCV**: YOLOv3 inference and image processing
- **NumPy**: Numerical computations and grid operations
- **PyTorch/TensorFlow**: Deep learning model support
- **HTML5/CSS3/JavaScript**: Interactive web dashboard

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Create a Pull Request

---

## 📝 License

This project is open source and available under the MIT License.

---

## 📧 Support & Questions

For issues, feature requests, or questions:
- Open an issue on GitHub
- Review existing documentation
- Check the project examples

---

## 🎓 Educational Use

This system is designed for:
- ✅ AI/ML research and experimentation
- ✅ Autonomous vehicle algorithm development
- ✅ Real-time system design study
- ✅ Computer vision application
- ✅ Path planning algorithm visualization

---

## 🏆 Acknowledgments

Built with state-of-the-art open-source libraries:
- Pygame Community
- OpenCV Team
- PyTorch & TensorFlow Communities
- YOLO/Darknet Creators

---

**Designed for AI experimentation, algorithm visualization, and automated prototyping.**

*Last Updated: 2026-05-25*
