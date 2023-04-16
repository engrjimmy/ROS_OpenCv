#!/usr/bin/env python3
 
import rospy 
from sensor_msgs.msg import Image 
from cv_bridge import CvBridge 
import cv2 
from tkinter import CENTER, Frame
import numpy as np 

cap = cv2.VideoCapture(0)
def cb_depth(self, data):
  frame = self.br.imgmsg_to_cv2(data, 'bgr8')
  
while(cap.isOpened()):
    ret, frame = cap.read()

    #Rectangle
    image_width = frame.shape[1]
    image_height = frame.shape[0]
    rect_width = image_width / 4
    rect_height = image_height / 4
    top_left_x = int(image_width / 2 - rect_width / 2)
    top_left_y = int(image_height / 2 - rect_height / 2)
    bottom_right_x = int(image_width / 2 + rect_width / 2)
    bottom_right_y = int(image_height / 2 + rect_height / 2)
    print("top left: {},{}   bottom right: {},{}".format(top_left_x, top_left_y, bottom_right_x, bottom_right_y))
    frame = cv2.rectangle(frame,
                          (top_left_x, top_left_y),
                          (bottom_right_x, bottom_right_y),
                          (0,255,0),
                          10)

    cv2.imshow('frame', frame)

    if cv2.waitKey(33) >= 0:
        break

    last_frame = frame

cap.release()
ret, last_frame = cap.read()

if last_frame is None:
    exit()
    
def publish_message():
 
  pub = rospy.Publisher('video_frames', Image, queue_size=10)
     
  rospy.init_node('video_pub_py', anonymous=True)
     
  rate = rospy.Rate(10) # 10hz per times loops
     
  cap = cv2.VideoCapture(0)
     
  # converting ros and cv bridge 
  br = CvBridge()
 
  # While ROS is still running.
  while not rospy.is_shutdown():
     
      # Capture frame-by-frame
      # This method returns True/False as well
      # as the video frame.
      ret, frame = cap.read()
         
      if ret == True:
        # Print debugging information to the terminal
        rospy.loginfo('publishing video frame')
             
        # Publish the image.
        # The 'cv2_to_imgmsg' method converts an OpenCV
        # image to a ROS image message
        pub.publish(br.cv2_to_imgmsg(frame))
             
      # Sleep just enough to maintain the desired rate
      rate.sleep()
         
if __name__ == '__main__':
  try:
    publish_message()
  except rospy.ROSInterruptException:
    pass
