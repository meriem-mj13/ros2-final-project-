
 TERMINAL 1 : RVIZ
source ~/ros2_ws/install/setup.bash
ros2 launch my_robot display.launch.py

 Terminal 2 — YOLO detection:
source ~/ros2_ws/install/setup.bash
ros2 run my_robot yolo_detector.py

 Terminal 3 — Robot controller:
source ~/ros2_ws/install/setup.bash
ros2 run my_robot move_robot.py

 Terminal 4 — Show cmd_vel live (axes):
ros2 topic echo /cmd_vel

 Terminal 5 — Show detections live:
ros2 topic echo /detections
