#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from ultralytics import YOLO
import cv2

class YoloDetector(Node):
    def __init__(self):
        super().__init__('yolo_detector')
        
        self.detection_pub = self.create_publisher(String, '/detections', 10)
        
        self.model_general = YOLO('/home/mirin/Downloads/p/yolov8n.pt')
        self.model_guitar = YOLO('/home/mirin/best.pt')
        
        self.cap = cv2.VideoCapture(0)
        self.timer = self.create_timer(0.1, self.detect)
        self.get_logger().info('YOLO detector started!')

    def detect(self):
        success, frame = self.cap.read()
        if not success:
            return

        results_general = self.model_general(frame, verbose=False)
        results_guitar = self.model_guitar(frame, verbose=False)

        detected = []

        # General detections (green boxes)
        for box in results_general[0].boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            cls = int(box.cls[0])
            label = results_general[0].names[cls]
            detected.append(f"{label}:{conf:.2f}")
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1-5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Guitar detections (red boxes) — only above 70% confidence
        guitar_detected = False
        for box in results_guitar[0].boxes:
            conf = float(box.conf[0])
            if conf < 0.7:
                continue
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            detected.append(f"guitar:{conf:.2f}")
            guitar_detected = True
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(frame, f"guitar {conf:.2f}", (x1, y1-5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # Show warning on screen when guitar detected
        if guitar_detected:
            cv2.putText(frame, 'FRAGILE OBJECT - SLOWING DOWN', (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        # Publish detections
        msg = String()
        msg.data = ','.join(detected) if detected else 'none'
        self.detection_pub.publish(msg)

        cv2.imshow('Museum Robot - YOLO Detection', frame)
        cv2.waitKey(1)

    def destroy_node(self):
        self.cap.release()
        cv2.destroyAllWindows()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = YoloDetector()
    rclpy.spin(node)

if __name__ == '__main__':
    main()