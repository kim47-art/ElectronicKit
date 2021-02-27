#!/usr/bin/python

# MIT License
# 
# Copyright (c) 2017 John Bryan Moore
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import math

import VL53L0X


import rospy
from sensor_msgs.msg import LaserScan

def setup():
    rospy.init_node('distance_sensor', anonymous=True)
    pass

def main():
    # Create a VL53L0X object
    tof = VL53L0X.VL53L0X()

    # Start ranging
    tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

    #timing = tof.get_timing()
    #if (timing < 20000):
    #    timing = 20000
    #rospy.loginfo("Timing %d ms" % (timing/1000))

    pub = rospy.Publisher('lider_scan', LaserScan, queue_size=10)
    laser_scan = LaserScan()
    laser_scan.header.seq = 0
    laser_scan.header.stamp = rospy.get_rostime()
    laser_scan.header.frame_id = "/world"
    laser_scan.angle_min = 0.0
    laser_scan.angle_max = math.pi
    laser_scan.angle_increment = math.pi/180
    laser_scan.time_increment = 1.0/180
    laser_scan.scan_time = laser_scan.time_increment * 360
    laser_scan.range_min = 0.1
    laser_scan.range_max = 2.0    

    r = rospy.Rate(90)
    angle = 0
    while not rospy.is_shutdown():
        laser_scan.ranges.append(float(tof.get_distance())/1000)
        
        if (angle >= 179):
            rospy.loginfo("pub")
            laser_scan.header.seq += 1
            laser_scan.header.stamp = rospy.get_rostime()
            pub.publish(laser_scan)
            laser_scan.ranges=[]
            angle = 0
        angle += 1
        r.sleep()

    tof.stop_ranging()

if __name__ == '__main__':
    setup()
    try:
        main()
    except rospy.ROSInterruptException:
        pass
