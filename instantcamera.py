import time
import picamera
#from datetime import datetime
from PIL import Image
import RPi.GPIO
import io
import os
pin = 7
flag=0
RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(pin,RPi.GPIO.IN)

camera = picamera.PiCamera()

def newimage() :
        camera.capture('/home/pi/inst.jpg')
        print "captured "
while 1:

	if  RPi.GPIO.input(pin)!=1:    #if the level is high, take N pictures
		print('HIGH')
