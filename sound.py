import RPi.GPIO as GPIO
import time
GPIO.cleanup()
time.sleep(1)

# GPIO SETUP
sound = 7
led = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(sound, GPIO.IN)
#GPIO.setup(led, GPIO.OUT)


def callback(sound):
    if GPIO.input(sound):
        print("Sound Detected!")
        # GPIO.output(led,HIGH)
    else:
        print("Sound Detected! else ")

        # GPIO.output(led,LOW)

# let us know when the pin goes HIGH or LOW


# infinite loop
while True:
    if GPIO.input(sound):
        print("Sound Detected!")
        # GPIO.output(led,HIGH)
    else:
        print("Sound Detected! else ")