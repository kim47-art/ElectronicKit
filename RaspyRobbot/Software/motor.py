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

#gpio_pin
MOTOR_PARAM = [
     {"gpio_pin_no":4, "pwm_max":1900, "pwm_min":1400,"cw":True},#1
     {"gpio_pin_no":14, "pwm_max":1750, "pwm_min":1000,"cw":True},#B
     {"gpio_pin_no":15, "pwm_max":2000, "pwm_min":1300,"cw":False},#2
     {"gpio_pin_no":17, "pwm_max":1000, "pwm_min":600,"cw":False},#A
     {"gpio_pin_no":18, "pwm_max":1600, "pwm_min":750,"cw":True},#3
     {"gpio_pin_no":22, "pwm_max":1000, "pwm_min":600,"cw":False},#4
     {"gpio_pin_no":23, "pwm_max":2300, "pwm_min":1900,"cw":True},#D
     {"gpio_pin_no":27, "pwm_max":2250, "pwm_min":1300,"cw":False},#C
]


#真横が0度、下が90度
class Motor:
     def __init__(self,pin):
          self.pi = pigpio.pi()
          self.pin=pin
          self.pwm_max=[x['pwm_max'] for x in MOTOR_PARAM if x['gpio_pin_no'] == self.pin][0]
          self.pwm_min=[x['pwm_min'] for x in MOTOR_PARAM if x['gpio_pin_no'] == self.pin][0]
          self.cw=[x['cw'] for x in MOTOR_PARAM if x['gpio_pin_no'] == self.pin][0]

     def sync_rotate(self,degree):#
          if(degree < 0 or degree >90):
               return
          
          diff=(self.pwm_max-self.pwm_min)/90*degree
          
          if(self.cw):
               pwm_val=self.pwm_min+diff
          else:
               pwm_val=self.pwm_max-diff

          print(pwm_val)
          self.pi.set_servo_pulsewidth(self.pin,pwm_val)

     def async_rotate(self,degree,elaps_time_msec):#
          pi.set_servo_pulsewidth(motor_B,1000)
          


