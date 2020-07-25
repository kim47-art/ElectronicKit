#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import pigpio
import time

motor_A=17
motor_B=14
motor_C=27
motor_D=23

motor_1=4
motor_2=15
motor_3=18
motor_4=22

#550~2350
pin=motor_D
pi = pigpio.pi()
#ここで-90
pi.set_servo_pulsewidth(pin,2300)
time.sleep(1)
#ここで0
#pi.set_servo_pulsewidth(pin, 1000)
#time.sleep(3)
