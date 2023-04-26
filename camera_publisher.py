#!/usr/bin/env python

import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

def camera_publisher():
    # Initialize the node
    rospy.init_node('camera_publisher', anonymous=True)

    # Create a publisher that publishes images to the "camera" topic
    pub = rospy.Publisher('camera', Image, queue_size=10)

    # Initialize the OpenCV camera capture
    cap = cv2.VideoCapture(0)

    # Check if the camera was opened successfully
    if not cap.isOpened():
        rospy.logerr("Error opening camera")
        return

    # Set the frame size of the video capture
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # Initialize the CvBridge object
    bridge = CvBridge()

    # Read the frames from the camera and publish them
    while not rospy.is_shutdown():
        # Read a frame from the camera
        ret, frame = cap.read()

        # Check if a frame was successfully read
        if not ret:
            rospy.logwarn("Failed to read frame from camera")
            continue

        # Convert the OpenCV image to a ROS image message
        try:
            image_msg = bridge.cv2_to_imgmsg(frame, "bgr8")
        except CvBridgeError as e:
            rospy.logerr(e)
            continue

        # Publish the image message to the "camera" topic
        pub.publish(image_msg)

    # Release the camera
    cap.release()

if __name__ == '__main__':
    try:
        camera_publisher()
    except rospy.ROSInterruptException:
        pass
