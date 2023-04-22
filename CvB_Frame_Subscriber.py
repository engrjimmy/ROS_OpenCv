#!/usr/bin/env python3
import rospy 
from sensor_msgs.msg import Image 
from cv_bridge import CvBridge 
import cv2 
 
class FrameImagePublisher:
  def callback(self, data):
    rospy.loginfo("receiving video frame")
    
    # Convert ROS Image message to OpenCV image
    frame = self.br.imgmsg_to_cv2(data, 'bgr8')
    
    # Draw rectangle
    image_width = frame.shape[1]
    image_height = frame.shape[0]
    rect_width = image_width / 4
    rect_height = image_height / 4
    top_left_x = int(image_width / 2 - rect_width / 2)
    top_left_y = int(image_height / 2 - rect_height / 2)
    bottom_right_x = int(image_width / 2 + rect_width / 2)
    bottom_right_y = int(image_height / 2 + rect_height / 2)
    frame = cv2.rectangle(frame,
                          (top_left_x, top_left_y),
                          (bottom_right_x, bottom_right_y),
                          (0,255,0),
                          10)
    # Publish image
    self.img_pub.publish(self.br.cv2_to_imgmsg(frame))
        
  def __init__(self):
    # init CV bridge
    self.br = CvBridge()
    
    # Set up subscriber and publisher
    self.img_sub = rospy.Subscriber('video_frames', Image, self.callback)
    self.img_pub = rospy.Publisher('image_with_frame', Image, queue_size=10)
    
if __name__ == '__main__':
  rospy.init_node('frame_image_publisher')
  fp = FrameImagePublisher()
  rospy.spin()
