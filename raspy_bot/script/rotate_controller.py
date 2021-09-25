#!/usr/bin/env python
# -*- coding: utf-8 -*-
# license removed for brevity
import pigpio

import rospy

from std_msgs.msg import Int16


light_val = 0
servo = 5
pi = pigpio.pi()

def callback_val_light_sensor(data):
    global light_val
    light_val=data.data

#setup function for some setup---custom function
def setup():
    global pi
    
    # モータピンを出力に設定
    pi.set_mode(servo, pigpio.OUTPUT)

    rospy.init_node('temp', anonymous=True)
    # 光センサのサブスクライブ設定
    rospy.Subscriber("val_light_sensor", Int16, callback_val_light_sensor)

    pass

def temp():
    global pi
    r = rospy.Rate(40)

    SERVO_PULSEWIDTH_DIFF_MAX  = 300
    SERVO_PULSEWIDTH_DIFF_MIN  = 100 
    SERVO_PULSEWIDTH_STOP = 1500

    KP = 30
    KI = 300
    KD = 0.1
    TARGET = rospy.Duration.from_sec(2.0) #目標は1周2秒

    servo_pulsewidth_diff = 200
    pi.set_servo_pulsewidth(servo,SERVO_PULSEWIDTH_STOP-servo_pulsewidth_diff)
    rospy.sleep(1.0)
    preP = rospy.get_rostime().to_sec()
    now = rospy.Time.now()
    I = 0
    while not rospy.is_shutdown():
        elapsed_time = rospy.Time.now() - now
        if(light_val >=90 and elapsed_time >= rospy.Duration.from_sec(0.5)):
            rospy.loginfo("elapsed_time:{0}".format(elapsed_time.to_sec()) + "[sec]")
            now = rospy.Time.now()
            
            P = (TARGET - elapsed_time).to_sec()
            I += P * P
            D = (P - preP) / P
            preP = P
            servo_pulsewidth_diff += ((KP * P) + (KI * I) + (KD * D)) *(-1.0) #TODO:調整
            rospy.loginfo("servo_pulsewidth_diff:{0}".format(servo_pulsewidth_diff))
            if(servo_pulsewidth_diff >= SERVO_PULSEWIDTH_DIFF_MAX):
                servo_pulsewidth_diff = SERVO_PULSEWIDTH_DIFF_MAX
            if(servo_pulsewidth_diff <= SERVO_PULSEWIDTH_DIFF_MIN):
                servo_pulsewidth_diff = SERVO_PULSEWIDTH_DIFF_MIN

        pi.set_servo_pulsewidth(servo,SERVO_PULSEWIDTH_STOP-servo_pulsewidth_diff)
        
        r.sleep()


    pi.set_servo_pulsewidth(servo, SERVO_PULSEWIDTH_STOP)

if __name__ == '__main__':
    setup()
    try:
        temp()
    except rospy.ROSInterruptException:
        pi.set_servo_pulsewidth(servo, SERVO_PULSEWIDTH_STOP)
        pass