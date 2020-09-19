#!/usr/bin/env python
<<<<<<< Updated upstream
# coding: utf-8
=======
# -*- coding: utf-8 -*-
>>>>>>> Stashed changes
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
    
    def set_allmotor(self,param):
        self.FLI.sync_rotate(param[0])
        self.FLO.sync_rotate(param[1])
        self.BLI.sync_rotate(param[2])
        self.BLO.sync_rotate(param[3])
        self.FRI.sync_rotate(param[4])
        self.FRO.sync_rotate(param[5])
        self.BRI.sync_rotate(param[6])
        self.BRO.sync_rotate(param[7])
        time.sleep(param[8])

class MoveSequenceItr(object):
    def __init__(self,sequence):
        self._sequence = sequence
        self._i = 0
    def __iter__(self):
        # __next__()はselfが実装してるのでそのままselfを返す
        return self
    def __next__(self):  # Python2だと next(self) で定義
        if self._i == len(self._sequence):
            #raise StopIteration()
            self._i=0
        value = self._sequence[self._i]
        self._i += 1
        return value


class MotorThread(threading.Thread):
    def __init__(self,move_sequence):
        super(MotorThread,self).__init__()
        self.moter_if= Moter_IF()
        self.started = threading.Event()
        self.alive = True
        self.move_sequence=MoveSequenceItr(move_sequence)
        self.start()

    def __del__(self):
        self.kill()

    def begin(self):
        #print("back begin")
        self.started.set()

    def end(self):
        self.started.clear()
        #print("\nback end")

    def kill(self):
        self.started.set()
        self.alive = False
        self.join()

    def run(self):
        self.started.wait()

        while self.alive:        
            self.moter_if.set_allmotor(self.move_sequence.__next__())
            self.started.wait()

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
        print("back end")

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


class Move_driver():
    def __init__(self):
        self.cmd_vel=Twist()

        self.forward_sequence=[ [ 0,70,90,90, 0,90,90,70,0.3],
                                [90,70,90,90, 0,90, 0,70,0.3],
                                [90,90,90,90, 0,90, 0,90,0.3],
                                [ 0,90, 0,70,90,70,90,90,0.3],
                                [ 0,90, 0,90,90,90,90,90,0.3]]

        self.back_sequence=[[90,90, 0,70,90,70, 0,90,0.3],
                            [90,90,90,70, 0,70, 0,90,0.3],
                            [90,90,90,90, 0,90, 0,90,0.3],
                            [ 0,70, 0,90,90,90,90,70,0.3],
                            [ 0,90, 0,90,90,90,90,90,0.3]]


        self.forward=MotorThread(self.forward_sequence)
        self.back=MotorThread(self.back_sequence)
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
            #if(self.cmd_vel.linear.x != -2.0):
            #    self.back.end()
            #else:
            #    self.back.begin()
            
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
