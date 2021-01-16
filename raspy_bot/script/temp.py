#!/usr/bin/env python
# -*- coding: utf-8 -*-
# license removed for brevity
import pigpio

import rospy
from std_msgs.msg import Int16

light_val = 0
servo = 5
pi = pigpio.pi()

def callback(data):
    global light_val
    light_val=data.data

#setup function for some setup---custom function
def setup():
    global pi
    
    # ピンを出力に設定
    pi.set_mode(servo, pigpio.OUTPUT)

    rospy.init_node('temp', anonymous=True)
    # 光センサのサブスクライブ設定
    rospy.Subscriber("val_light_sensor", Int16, callback)

    pass

def temp():
    global pi
    r = rospy.Rate(10) # 10hz
    pi.set_servo_pulsewidth(servo, 1400)
    rospy.sleep(1.0)
    while not rospy.is_shutdown():
        #pi.set_servo_pulsewidth(servo, 1400)
        #rospy.loginfo(str)
        rospy.loginfo(rospy.get_caller_id()+"I heard %d",light_val)
        
        if(light_val >=90 ):
            break

        r.sleep()
    pi.set_servo_pulsewidth(servo, 1500)

if __name__ == '__main__':
    setup()
    try:
        temp()
    except rospy.ROSInterruptException: pass