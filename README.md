# Museum Autonomous Security & Cleaning Robot — ROS2

## Project Description
Autonomous robot designed for museum environments. Activates at night to clean and secure the premises using LiDAR navigation and YOLO object detection.

## Features
- Autonomous patrol using cmd_vel
- Fragile artifact detection using custom trained YOLOv8 model (guitar)
- Intruder detection using general YOLOv8 model
- Real time ROS2 topic communication
- Security alert system

## Tech Stack
- ROS2 Jazzy
- YOLOv8 (Ultralytics)
- Python
- RViz

## Robot Sensors (Simulated)
- Mecanum wheels (omnidirectional)
- LiDAR sensor
- RGB Camera

## How it works
- yolo_detector.py reads camera feed, runs two YOLO models, publishes to /detections topic
- move_robot.py subscribes to /detections, publishes velocity commands to /cmd_vel
- Guitar detected → robot stops and turns away (fragile object protection)
- Person detected at night → intruder alert triggered
- Nothing detected → normal patrol continues

## Run the project

### 1. Build the package
cd ~/ros2_ws
colcon build --packages-select my_robot
source ~/ros2_ws/install/setup.bash

### 2. Terminal 1 — Launch robot in RViz
source ~/ros2_ws/install/setup.bash
ros2 launch my_robot display.launch.py

### 3. Terminal 2 — Start YOLO detector
source ~/ros2_ws/install/setup.bash
ros2 run my_robot yolo_detector.py

### 4. Terminal 3 — Start robot controller
source ~/ros2_ws/install/setup.bash
ros2 run my_robot move_robot.py

### 5. Terminal 4 — Monitor velocity commands
ros2 topic echo /cmd_vel

### 6. Terminal 5 — Monitor detections
ros2 topic echo /detections

## Robot Behavior
| Detection | Robot Response |
|-----------|---------------|
| Nothing | Move forward (linear.x: 0.2) |
| Guitar (fragile object) | Stop + turn away (linear.x: 0.0, angular.z: 0.3) |
| Person (intruder) | Keep patrolling + send alert |

## Project Structure
my_robot/
├── urdf/
│   └── robot.urdf          # Robot description
├── launch/
│   └── display.launch.py   # Launch file for RViz
├── scripts/
│   ├── yolo_detector.py    # YOLO detection node
│   └── move_robot.py       # Robot controller node
├── CMakeLists.txt
└── package.xml
