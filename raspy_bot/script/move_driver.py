#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
import pigpio
import time
import motor
# https://makezine.jp/blog/2016/12/robot-quadruped-arduino-program.html



class Move_driver():
    def __init__(self):
        self.FLO=motor.Motor(motor.Motor.motor_B)#FrontLightOutside
        self.FLI=motor.Motor(motor.Motor.motor_A)#FrontLightInside
        self.BLO=motor.Motor(motor.Motor.motor_C)
        self.BLI=motor.Motor(motor.Motor.motor_D)

        self.FRO=motor.Motor(motor.Motor.motor_2)
        self.FRI=motor.Motor(motor.Motor.motor_1)
        self.BRO=motor.Motor(motor.Motor.motor_3)
        self.BRI=motor.Motor(motor.Motor.motor_4)
    
        self.cmd_vel=Twist()
        rospy.Subscriber("/turtle1/cmd_vel", Twist, self.callback)

    def callback(self,data):
        #rospy.loginfo(data)
        self.cmd_vel=data

    def stop(self):
        self.FLI.sync_rotate(0)
        self.FLO.sync_rotate(90)
        self.BLI.sync_rotate(0)
        self.BLO.sync_rotate(90)
        self.FRI.sync_rotate(0)
        self.FRO.sync_rotate(90)
        self.BRI.sync_rotate(0)
        self.BRO.sync_rotate(90)

    def step_left_1(self):
        self.FLI.sync_rotate(70)
        self.FLO.sync_rotate(90)
        self.BLI.sync_rotate(70)
        self.BLO.sync_rotate(90)
        self.FRI.sync_rotate(0)
        self.FRO.sync_rotate(90)
        self.BRO.sync_rotate(60)
        time.sleep(0.1)
        self.BRI.sync_rotate(90)
        time.sleep(0.1)
        self.BRI.sync_rotate(0)
        self.BRO.sync_rotate(90)


    def step_left_2(self):
        self.FLI.sync_rotate(70)
        self.FLO.sync_rotate(90)
        self.BLI.sync_rotate(70)
        self.BLO.sync_rotate(90)
        self.FRI.sync_rotate(0)
        self.FRO.sync_rotate(60)
        self.BRI.sync_rotate(0)
        self.BRO.sync_rotate(90)

        time.sleep(0.1)
        self.FRI.sync_rotate(80)

    def move_1(self):
        self.FLI.sync_rotate(0)
        self.FLO.sync_rotate(90)
        self.BLI.sync_rotate(90)
        self.BLO.sync_rotate(90)
        self.FRI.sync_rotate(30)
        self.FRO.sync_rotate(90)
        self.BRI.sync_rotate(80)
        self.BRO.sync_rotate(90)

    def step_right_1(self):
        self.FLI.sync_rotate(0)
        self.FLO.sync_rotate(90)
        self.BLI.sync_rotate(90)
        self.BLO.sync_rotate(60)
        self.FRI.sync_rotate(30)
        self.FRO.sync_rotate(90)
        self.BRI.sync_rotate(80)
        self.BRO.sync_rotate(90)
        time.sleep(0.1)
        self.BLI.sync_rotate(0)
        time.sleep(0.1)
        self.BLO.sync_rotate(90)

    def step_right_2(self):
        self.FLI.sync_rotate(0)
        self.FLO.sync_rotate(60)
        self.BLI.sync_rotate(0)
        self.BLO.sync_rotate(90)
        self.FRI.sync_rotate(30)
        self.FRO.sync_rotate(90)
        self.BRI.sync_rotate(80)
        self.BRO.sync_rotate(90)
        time.sleep(0.1)
        self.FLI.sync_rotate(90)

    def move_2(self):
        self.FLI.sync_rotate(30)
        self.FLO.sync_rotate(90)
        self.BLI.sync_rotate(60)
        self.BLO.sync_rotate(60)
        self.FRI.sync_rotate(0)
        self.FRO.sync_rotate(90)
        self.BRI.sync_rotate(90)
        self.BRO.sync_rotate(90)

    def side1(self):
        self.FLI.sync_rotate(0)
        self.FLO.sync_rotate(45)
        self.BLI.sync_rotate(0)
        self.BLO.sync_rotate(45)
        time.sleep(0.5)

    def side2(self):
        self.FLI.sync_rotate(0)
        self.FLO.sync_rotate(90)
        self.BLI.sync_rotate(0)
        self.BLO.sync_rotate(90)
        self.FRI.sync_rotate(0)
        self.FRO.sync_rotate(60)
        self.BRI.sync_rotate(0)
        self.BRO.sync_rotate(60)
        time.sleep(0.5)
    def stop2(self):
        self.FLI.sync_rotate(90)
        self.FLO.sync_rotate(0)
        self.BLI.sync_rotate(90)
        self.BLO.sync_rotate(0)
        self.FRI.sync_rotate(90)
        self.FRO.sync_rotate(0)
        self.BRI.sync_rotate(90)
        self.BRO.sync_rotate(0)
        time.sleep(0.5)

    def run(self):
        self.stop2()
        
        rate = rospy.Rate(10) # 10hz
        while not rospy.is_shutdown():
            break
            rate.sleep()
            if(self.cmd_vel.linear.x != 2.0):
                self.stop()
            else:
                #step1
                self.step_left_1()
                time.sleep(0.5)
                if(self.cmd_vel.linear.x != 2.0):
                    continue

                #step2 
                self.step_left_2()
                time.sleep(0.1)
                if(self.cmd_vel.linear.x != 2.0):
                    continue

                #move
                self.move_1()
                time.sleep(0.5)
                if(self.cmd_vel.linear.x != 2.0):
                    continue

                #step3
                self.step_right_1()
                time.sleep(0.5)
                if(self.cmd_vel.linear.x != 2.0):
                    continue

                #step4
                self.step_right_2()
                time.sleep(0.1)
                if(self.cmd_vel.linear.x != 2.0):
                    continue

                #move
                self.move_2()
                time.sleep(0.5)
                if(self.cmd_vel.linear.x != 2.0):
                    continue






            
        


if __name__ == '__main__':
    try:
        rospy.init_node('move_driver', anonymous=True)
        move_driver=Move_driver()
        move_driver.run()
    except rospy.ROSInterruptException:
        rospy.loginfo("ROSInterruptException")
        move_driver.stop()
        pass