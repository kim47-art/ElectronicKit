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



#足上げ
def sit_down(pi):
     pi.set_servo_pulsewidth(motor_B,1000)
     pi.set_servo_pulsewidth(motor_C,2150)
     pi.set_servo_pulsewidth(motor_3,750)
     pi.set_servo_pulsewidth(motor_2,2100)
#立つ
def stand(pi):
     pi.set_servo_pulsewidth(motor_B,1750)
     pi.set_servo_pulsewidth(motor_C,1300)
     pi.set_servo_pulsewidth(motor_3,1600)
     pi.set_servo_pulsewidth(motor_2,1300)
#550~2350
pi = pigpio.pi()

sit_down(pi)
time.sleep(3)
stand(pi)
time.sleep(3)
sit_down(pi)
