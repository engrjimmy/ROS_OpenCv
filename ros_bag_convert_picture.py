#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2016 Massachusetts Institute of Technology
#Author: Jimmy Majumder 

"""Extract images from a rosbag.
"""

import os
import argparse
import cv2
import glob
import rosbag
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

def main():
    """Extract a folder of images from a rosbag.
    """
    path = '*.bag'
    files = glob.glob(path)
    for file in files:
        # parser = argparse.ArgumentParser(description="Extract images from a ROS bag.")
        # parser.add_argument("bag_file", help="Input ROS bag.")

        # args = parser.parse_args()
        

        output_dir = "./"+file
        bag = rosbag.Bag(file, "r")
        bridge = CvBridge()
        count = 0
        image_topic ='/left_arm_camera/color/image_raw'
        dir_name = (''.join(output_dir.split('.')[:-1])[1:])
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)

        for topic, msg, t in bag.read_messages(topics=[image_topic]):
            cv_img = bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")

            cv2.imwrite(os.path.join(dir_name,dir_name+"_%i.png" % count), cv_img)
            print(file, count)
            # print("Wrote image %i" % count)

            count += 1

        bag.close()

    return

if __name__ == '__main__':
    main()
