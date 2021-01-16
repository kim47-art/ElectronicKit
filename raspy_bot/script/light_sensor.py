#!/usr/bin/env python
# coding: utf-8
import rospy
from std_msgs.msg import Int16

import RPi.GPIO as GPIO

# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8
#set BCM_GPIO 18(GPIO1) as LED pin
LEDPIN = 18

analogChannel = 0

#setup function for some setup---custom function
def setup():
    GPIO.setwarnings(False)
    #set the gpio modes to BCM numbering
    GPIO.setmode(GPIO.BCM)
    # set up the SPI interface pins
    GPIO.setup(SPIMOSI, GPIO.OUT)
    GPIO.setup(SPIMISO, GPIO.IN)
    GPIO.setup(SPICLK, GPIO.OUT)
    GPIO.setup(SPICS, GPIO.OUT)
    pass

    

# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)

        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1

        GPIO.output(cspin, True)
        
        adcout >>= 1       # first bit is 'null' so drop it
        return adcout

#main function
def main():
    pub = rospy.Publisher('val_light_sensor', Int16, queue_size=10)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        rate.sleep()
        adc = readadc(analogChannel, SPICLK, SPIMOSI, SPIMISO, SPICS)
        adc =(1023-adc)*100/1023
        # rospy.loginfo('val_light_sensor = %d',adc)
        pub.publish(adc)

#define a destroy function for clean up everything after the script finished
def destroy():
    #stop p
    p.stop()
    #turn off led
    GPIO.output(LEDPIN,GPIO.LOW)
    #release resource
    GPIO.cleanup()
    

if __name__ == '__main__':
    setup()
    try:
        rospy.init_node('light_sensor', anonymous=True)
        main()
    #when 'Ctrl+C' is pressed,child program destroy() will be executed.
    except rospy.ROSInterruptException:
        rospy.loginfo("ROSInterruptException")
        destroy()

