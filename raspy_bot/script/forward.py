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


def set_allmotor(param,sleep_sec):
    front_left_leg.sync_rotate(param[0])
    front_left_knee.sync_rotate(param[1])
    rear_left_leg.sync_rotate(param[2])
    rear_left_knee.sync_rotate(param[3])
    front_right_leg.sync_rotate(param[4])
    front_right_knee.sync_rotate(param[5])
    rear_right_leg.sync_rotate(param[6])
    rear_right_knee.sync_rotate(param[7])
    time.sleep(sleep_sec)

set_allmotor([ 0,90,90,90, 0,90,90,90],0.5)

for i in range(5):

    set_allmotor([ 0,70,90,90, 0,90,90,70],0.3)
    set_allmotor([90,70,90,90, 0,90, 0,70],0.3)
    set_allmotor([90,90,90,90, 0,90, 0,90],0.3)
    set_allmotor([ 0,90, 0,70,90,70,90,90],0.3)
    set_allmotor([ 0,90, 0,90,90,90,90,90],0.3)
