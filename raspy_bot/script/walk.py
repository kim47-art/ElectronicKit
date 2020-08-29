#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import pigpio
import time
import motor

#def stand_up():

front_left_knee=motor.Motor(motor.Motor.motor_B)
front_left_leg=motor.Motor(motor.Motor.motor_A)
rear_left_knee=motor.Motor(motor.Motor.motor_C)
rear_left_leg=motor.Motor(motor.Motor.motor_D)

front_right_knee=motor.Motor(motor.Motor.motor_2)
front_right_leg=motor.Motor(motor.Motor.motor_1)
rear_right_knee=motor.Motor(motor.Motor.motor_3)
rear_right_leg=motor.Motor(motor.Motor.motor_4)

front_left_leg.sync_rotate(0)
front_left_knee.sync_rotate(90)
rear_left_leg.sync_rotate(0)
rear_left_knee.sync_rotate(90)
front_right_leg.sync_rotate(0)
front_right_knee.sync_rotate(90)
rear_right_leg.sync_rotate(0)
rear_right_knee.sync_rotate(90)



for i in range(5):

    #step1
    front_left_leg.sync_rotate(70)
    front_left_knee.sync_rotate(90)
    rear_left_leg.sync_rotate(70)
    rear_left_knee.sync_rotate(90)
    front_right_leg.sync_rotate(0)
    front_right_knee.sync_rotate(90)
    rear_right_leg.sync_rotate(0)
    rear_right_knee.sync_rotate(90)
    time.sleep(0.5)    

    #break

    #step2 
    front_right_knee.sync_rotate(60)
    time.sleep(0.1)
    front_right_leg.sync_rotate(80)
    time.sleep(0.1)
    #front_right_knee.sync_rotate(90)  
    #time.sleep(1)


    #move
    front_left_leg.sync_rotate(0)
    front_right_leg.sync_rotate(30)
    front_right_knee.sync_rotate(90)
    rear_left_leg.sync_rotate(90)
    rear_right_leg.sync_rotate(80)
    time.sleep(0.5)


    #step3
    rear_left_knee.sync_rotate(60)
    time.sleep(0.1)
    rear_left_leg.sync_rotate(0)
    time.sleep(0.1)
    rear_left_knee.sync_rotate(90)
    time.sleep(0.5)


    #step4
    front_left_knee.sync_rotate(60)
    time.sleep(0.1)
    front_left_leg.sync_rotate(90)
    time.sleep(0.1)

    #move
    front_right_leg.sync_rotate(0)
    front_left_leg.sync_rotate(30)
    front_left_knee.sync_rotate(90)
    rear_right_leg.sync_rotate(90)
    rear_left_leg.sync_rotate(60)
    time.sleep(0.5)    

    #move->step1
    rear_right_knee.sync_rotate(60)
    time.sleep(0.1)
    rear_right_leg.sync_rotate(90)
    time.sleep(0.1)

front_left_leg.sync_rotate(0)
front_left_knee.sync_rotate(90)
rear_left_leg.sync_rotate(0)
rear_left_knee.sync_rotate(90)
front_right_leg.sync_rotate(0)
front_right_knee.sync_rotate(90)
rear_right_leg.sync_rotate(0)
rear_right_knee.sync_rotate(90)