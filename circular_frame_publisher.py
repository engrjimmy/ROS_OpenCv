#!/usr/bin/env python3

import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

def main():
    rospy.init_node("circular_frame_publisher")
    pub = rospy.Publisher("/camera/circular_frame", Image, queue_size=10)
    rate = rospy.Rate(10)  # Publish at 10 Hz
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    bridge = CvBridge()
    while not rospy.is_shutdown():
        ret, frame = cap.read()
        if not ret:
            break
        height, width, channels = frame.shape
        center_x, center_y = int(width/2), int(height/2)
        scaling_factor = 0.5  # Change this to adjust the size of the circle
        if width < height:
            radius = int(width * scaling_factor / 2)
        else:
            radius = int(height * scaling_factor / 2)
        cv2.circle(frame, (center_x, center_y), radius, (0, 255, 0), 2)
        pub.publish(bridge.cv2_to_imgmsg(frame, "bgr8"))
        cv2.imshow("Camera view", frame)
        cv2.waitKey(1)
        rate.sleep()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
