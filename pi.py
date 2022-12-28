#Libraries
import RPi.GPIO as GPIO
import time
import requests as re
import json 
import base64
import numpy as np
from picamera2 import Picamera2, Preview
import yaml
import matplotlib.image as mpimg
from PIL import Image
ip = "172.22.5.242"
picam2 = Picamera2()

preview_config = picam2.create_preview_configuration(main={"size": (1920, 1080)})
picam2.configure(preview_config)

picam2.start_preview(Preview.QTGL)

picam2.start()

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 21
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
def callback(sound):
    if GPIO.input(sound):
        print("Sound Detected!")
        time.sleep(3)
        print("You can talk after 5 seconds...")
        time.sleep(1)
        print("You can talk after 4 seconds...")
        time.sleep(1)
        print("You can talk after 3 seconds...")
        time.sleep(1)
        print("You can talk after 2 seconds...")
        time.sleep(1)
        print("You can talk after 1 seconds...")
        time.sleep(1)
        print("You can talk now...")
        # GPIO.output(led,HIGH)
    else:
        print("Sound Detected! else ")
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance

if __name__ == '__main__':
    try:
        while True:
            print("in the while")
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
            time.sleep(1)
            if(dist<50):
                picam2.capture_file("tmp.jpg")
                time.sleep(5) 
                try:    
                    time.sleep(2)   
                    is_it_us= re.post("http://"+ip+":5000/end_point_1a", files={'image': open('tmp.jpg', 'rb')})
                    if(is_it_us=="true"):
                        sound = 17
                        led = 27

                        GPIO.setmode(GPIO.BCM)
                        GPIO.setup(sound, GPIO.IN)
                        GPIO.setup(led, GPIO.OUT)
                        GPIO.add_event_detect(sound, GPIO.BOTH, bouncetime=300)
                        # assign function to GPIO PIN, Run function on change
                        GPIO.add_event_callback(sound, callback)

                        # infinite loop
                        while GPIO.input(sound)==False:
                            time.sleep(1)
                except:
                    print("Network error")
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
