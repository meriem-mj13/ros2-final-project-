cmake_minimum_required(VERSION 3.8)
project(my_robot)

find_package(ament_cmake REQUIRED)
find_package(rclpy REQUIRED)

install(
  DIRECTORY urdf launch scripts
  DESTINATION share/${PROJECT_NAME}
)

install(PROGRAMS
  scripts/move_robot.py
  scripts/yolo_detector.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()