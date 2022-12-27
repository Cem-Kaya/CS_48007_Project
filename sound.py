import RPi.GPIO as GPIO
import time

# GPIO SETUP
sound = 17
led = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(sound, GPIO.IN)
GPIO.setup(led, GPIO.OUT)


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

        # GPIO.output(led,LOW)

# let us know when the pin goes HIGH or LOW
GPIO.add_event_detect(sound, GPIO.BOTH, bouncetime=300)
# assign function to GPIO PIN, Run function on change
GPIO.add_event_callback(sound, callback)

# infinite loop
while True:
    time.sleep(1)
