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
import pyaudio
import wave
ip = "172.22.156.89"
picam2 = Picamera2()

preview_config = picam2.create_preview_configuration(main={"size": (1920, 1080)})
picam2.configure(preview_config)

picam2.start_preview(Preview.QTGL)

picam2.start()

#GPIO Mode (BOARD / BCM)
GPIO.cleanup()
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
            GPIO.setmode(GPIO.BCM)
 
            #set GPIO Pins
            GPIO_TRIGGER = 18
            GPIO_ECHO = 21
            
            #set GPIO direction (IN / OUT)
            GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
            GPIO.setup(GPIO_ECHO, GPIO.IN)
            print("in the while")
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
            time.sleep(1)
            if(dist<50):
                picam2.capture_file("tmp.jpg")
                time.sleep(5) 
                try:    
                    time.sleep(2)   
                    print("it is trying")
                    is_it_us= re.post("http://"+ip+":5000/end_point_1a", files={'image': open('tmp.jpg', 'rb')})
                    print("is_it_us ",is_it_us)
                    is_it_truly_us=is_it_us.text
                    print("is_it_truly_us ",is_it_truly_us)
                    try:
                        if("emre" in is_it_truly_us or "cem" in is_it_truly_us or "onur" in is_it_truly_us  ):
                            print("welcome: ", is_it_truly_us, " now we will take the password please wait ")
                            GPIO.cleanup()
                            print("in second while")
                            sound = 17
                            led = 27
                            
                           
                            GPIO.cleanup()
                            GPIO.setmode(GPIO.BCM)
                            GPIO.setup(sound, GPIO.IN)
                            GPIO.setup(led, GPIO.OUT)
                            GPIO.add_event_detect(sound, GPIO.BOTH, bouncetime=300)
                            # assign function to GPIO PIN, Run function on change
                            GPIO.add_event_callback(sound, callback)
                            print(" is it false",GPIO.input(sound))

                            # infinite loop
                            while GPIO.input(sound)==0:
                                print("please make a sound so we know you are ready to say the password")
                                time.sleep(1)
                            GPIO.cleanup()
                            form_1 = pyaudio.paInt16 # 16-bit resolution
                            chans = 1 # 1 channel
                            samp_rate = 44100 # 44.1kHz sampling rate
                            chunk = 4096 # 2^12 samples for buffer
                            record_secs = 18 # seconds to record
                            dev_index = 1# device index found by p.get_device_info_by_index(ii)
                            wav_output_filename = 'test1.wav' # name of .wav file

                            audio = pyaudio.PyAudio() # create pyaudio instantiation

                            # create pyaudio stream
                            stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                                                input_device_index = dev_index,input = True, \
                                                frames_per_buffer=chunk)
                            print("recording")
                            frames = []

                            # loop through stream and append audio chunks to frame array
                            for ii in range(0,int((samp_rate/chunk)*record_secs)):
                                data = stream.read(chunk)
                                frames.append(data)

                            print("finished recording")

                            # stop the stream, close it, and terminate the pyaudio instantiation
                            stream.stop_stream()
                            stream.close()
                            audio.terminate()

                            # save the audio frames as .wav file
                            wavefile = wave.open(wav_output_filename,'wb')
                            wavefile.setnchannels(chans)
                            wavefile.setsampwidth(audio.get_sample_size(form_1))
                            wavefile.setframerate(samp_rate)
                            wavefile.writeframes(b''.join(frames))
                            wavefile.close()
                            try:    
                                print( re.post("http://"+ip+":5000/end_point_3", files={'sound': open('test1.wav', 'rb')}) ) 
                                time.sleep(2) 
                            except Exception as e:
                                print("this expect is !!!!!! ",e)
                    except Exception as e:
                        print("expection is ..... ", e)
                            
                except:
                    print("Network error")
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
