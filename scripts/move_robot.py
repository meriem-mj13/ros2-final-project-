#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String

class MuseumRobotController(Node):
    def __init__(self):
        super().__init__('museum_robot_controller')
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.create_subscription(String, '/detections', self.detection_callback, 10)
        self.fragile_detected = False
        self.timer = self.create_timer(0.1, self.move)
        self.get_logger().info('Museum robot controller started!')

    def detection_callback(self, msg):
        detections = msg.data
        self.fragile_detected = 'guitar' in detections

        if 'person' in detections:
            self.get_logger().error('INTRUDER ALERT - HUMAN DETECTED IN MUSEUM!')

        if self.fragile_detected:
            self.get_logger().warn('Fragile object detected - stopping!')
        elif 'person' not in detections:
            self.get_logger().info('Path clear - patrolling...')

    def move(self):
        cmd = Twist()
        if self.fragile_detected:
            cmd.linear.x = 0.0
            cmd.angular.z = 0.3
        else:
            cmd.linear.x = 0.2
            cmd.angular.z = 0.0
        self.cmd_pub.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    node = MuseumRobotController()
    rclpy.spin(node)

if __name__ == '__main__':
    main()