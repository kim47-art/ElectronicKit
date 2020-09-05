#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
import pigpio
import time
import threading
import motor
# https://makezine.jp/blog/2016/12/robot-quadruped-arduino-program.html

class Moter_IF():
    def __init__(self):
        self.FLI=motor.Motor(motor.Motor.motor_A)#FrontLightInside
        self.FLO=motor.Motor(motor.Motor.motor_B)#FrontLightOutside
        self.BLI=motor.Motor(motor.Motor.motor_D)
        self.BLO=motor.Motor(motor.Motor.motor_C)
        self.FRI=motor.Motor(motor.Motor.motor_1)
        self.FRO=motor.Motor(motor.Motor.motor_2)
        self.BRI=motor.Motor(motor.Motor.motor_4)
        self.BRO=motor.Motor(motor.Motor.motor_3)
    
    def set_allmotor(self,param,sleep_sec):
        self.FLI.sync_rotate(param[0])
        self.FLO.sync_rotate(param[1])
        self.BLI.sync_rotate(param[2])
        self.BLO.sync_rotate(param[3])
        self.FRI.sync_rotate(param[4])
        self.FRO.sync_rotate(param[5])
        self.BRI.sync_rotate(param[6])
        self.BRO.sync_rotate(param[7])
        time.sleep(sleep_sec)

class BackThread(threading.Thread):
    def __init__(self):
        super(BackThread,self).__init__()
        self.moter_if= Moter_IF()
        self.started = threading.Event()
        self.alive = True
        self.start()

    def __del__(self):
        self.kill()

    def begin(self):
        print("back begin")
        self.started.set()

    def end(self):
        self.started.clear()
        print("\nback end")

    def kill(self):
        self.started.set()
        self.alive = False
        self.join()

    def run(self):
        self.started.wait()
        while self.alive:
            self.moter_if.set_allmotor([90,90, 0,70,90,70, 0,90],0.3)
            self.moter_if.set_allmotor([90,90,90,70, 0,70, 0,90],0.3)
            self.moter_if.set_allmotor([90,90,90,90, 0,90, 0,90],0.3)
            self.moter_if.set_allmotor([ 0,70, 0,90,90,90,90,70],0.3)
            self.moter_if.set_allmotor([ 0,90, 0,90,90,90,90,90],0.3)
            self.started.wait()


class ForwardThread(threading.Thread):
    def __init__(self):
        super(ForwardThread,self).__init__()
        self.moter_if= Moter_IF()
        self.started = threading.Event()
        self.alive = True
        self.start()

    def __del__(self):
        self.kill()

    def begin(self):
        print("forward begin")
        self.started.set()

    def end(self):
        self.started.clear()
        print("\nforward end")

    def kill(self):
        self.started.set()
        self.alive = False
        self.join()

    def run(self):
        self.started.wait()
        while self.alive:
            self.moter_if.set_allmotor([ 0,70,90,90, 0,90,90,70],0.3)
            self.started.wait()
            self.moter_if.set_allmotor([90,70,90,90, 0,90, 0,70],0.3)
            self.started.wait()
            self.moter_if.set_allmotor([90,90,90,90, 0,90, 0,90],0.3)
            self.started.wait()
            self.moter_if.set_allmotor([ 0,90, 0,70,90,70,90,90],0.3)
            self.started.wait()
            self.moter_if.set_allmotor([ 0,90, 0,90,90,90,90,90],0.3)
            self.started.wait()

class Move_driver():
    def __init__(self):
        self.cmd_vel=Twist()
        self.forward=ForwardThread()
        self.back=BackThread()
        rospy.Subscriber("/turtle1/cmd_vel", Twist, self.callback)

    def callback(self,data):
        #rospy.loginfo(data)
        self.cmd_vel=data


    def run(self):
        
        rate = rospy.Rate(10) # 10hz
        while not rospy.is_shutdown():
            rate.sleep()
            if(self.cmd_vel.linear.x != 2.0):
                self.forward.end()
            else:
                self.forward.begin()
            if(self.cmd_vel.linear.x != -2.0):
                self.back.end()
            else:
                self.back.begin()
            
        self.forward.end()
        self.forward.kill()
        self.back.end()
        self.back.kill()





            
        


if __name__ == '__main__':
    try:
        rospy.init_node('move_driver', anonymous=True)
        move_driver=Move_driver()
        move_driver.run()
    except rospy.ROSInterruptException:
        rospy.loginfo("ROSInterruptException")
        move_driver.stop()
        pass