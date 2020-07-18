#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import pigpio
import time
import motor



def stand_up

front_left_knee=motor.Motor(17)
front_left_leg=motor.Motor(14)
rear_left_knee=motor.Motor(27)
rear_left_leg=motor.Motor(23)

front_right_knee=motor.Motor(4)
front_right_leg=motor.Motor(15)
fron_right_knee=motor.Motor(18)
fron_right_leg=motor.Motor(22)



rear_left_leg.sync_rotate(0)
time.sleep(3)

