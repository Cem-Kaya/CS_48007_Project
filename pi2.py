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

#!/usr/bin/env python
from ctypes import *
import pyaudio

# From alsa-lib Git 3fd4ab9be0db7c7430ebd258f2717a976381715d
# $ grep -rn snd_lib_error_handler_t
# include/error.h:59:typedef void (*snd_lib_error_handler_t)(const char *file, int line, const char *function, int err, const char *fmt, ...) /* __attribute__ ((format (printf, 5, 6))) */;
# Define our error handler type
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
def py_error_handler(filename, line, function, err, fmt):
  pass
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

asound = cdll.LoadLibrary('libasound.so')
# Set error handler




picam2 = Picamera2()

preview_config = picam2.create_preview_configuration(main={"size": (1920, 1080)})
picam2.configure(preview_config)

picam2.start_preview(Preview.QTGL)

picam2.start()

#GPIO Mode (BOARD / BCM)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 21
GPIO_LED1=8
GPIO_LED2=10
#set GPIO direction (IN / OUT)
GPIO.setwarnings(False)
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
            GPIO.cleanup()
            GPIO.setmode(GPIO.BCM)
 
            #set GPIO Pins
            GPIO_TRIGGER = 18
            GPIO_ECHO = 21
            
            #set GPIO direction (IN / OUT)
           
            GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
            GPIO.setup(GPIO_ECHO, GPIO.IN)
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
            time.sleep(1)
            if(dist<25):
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
                            #GPIO.setwarnings(False)
                            
                            GPIO.setwarnings(False)
                          
                            sound = 15
                            
                            
                           
                            
                            GPIO.setmode(GPIO.BCM)
                            GPIO.setup(sound, GPIO.IN)
                            while True:
                                if GPIO.input(sound):
                                    print("Sound Detected now we will record you for your password!")
                                    break
                                    # GPIO.output(led,HIGH)
                                else:
                                    print("please make a sound so we will know you are ready")
                                    time.sleep(1)
                            asound.snd_lib_error_set_handler(c_error_handler)


                            form_1 = pyaudio.paInt16 # 16-bit resolution
                            chans = 1 # 1 channel
                            samp_rate = 44100 # 44.1kHz sampling rate
                            chunk = 4096 # 2^12 samples for buffer
                            record_secs = 20 # seconds to record
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
                            asound.snd_lib_error_set_handler(None)

                            # save the audio frames as .wav file
                            wavefile = wave.open(wav_output_filename,'wb')
                            wavefile.setnchannels(chans)
                            wavefile.setsampwidth(audio.get_sample_size(form_1))
                            wavefile.setframerate(samp_rate)
                            wavefile.writeframes(b''.join(frames))
                            wavefile.close()
                            try:    
                                pass_check= re.post("http://"+ip+":5000/end_point_3", files={'sound': open('test1.wav', 'rb')}) 
                                time.sleep(2) 
                                
                                if(pass_check.text=="true"):
                                    if("emre" in is_it_truly_us):
                                        print("led1")
                                        
                                        
                                        GPIO.setwarnings(False) # Ignore warning for now
                                        GPIO.cleanup()
                                        time.sleep(1)
                                        GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
                                        GPIO.setup(GPIO_LED2, GPIO.OUT, initial=GPIO.LOW) 
                                        GPIO.setup(GPIO_LED1, GPIO.OUT, initial=GPIO.LOW) 
                                        GPIO.output(GPIO_LED1, GPIO.HIGH) # Turn on
                                        print("now you can see your led, ", is_it_truly_us)
                                        time.sleep(10)

                                        time.sleep(10) # Sleep for 1 second
                                    elif("cem" in is_it_truly_us):
                                        time.sleep(1) # Sleep for 1 second
                                        
                                        GPIO.setwarnings(False) # Ignore warning for now
                                        GPIO.cleanup()
                                        time.sleep(1)
                                        GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
                                        GPIO.setup(GPIO_LED1, GPIO.OUT, initial=GPIO.LOW) 
                                       
                                        
                                        GPIO.setup(GPIO_LED2, GPIO.OUT, initial=GPIO.LOW) # Set pin 8 to be an output pin and >
                                      
                                        GPIO.output(GPIO_LED2, GPIO.HIGH) # Turn on
                                        
                                        GPIO.setwarnings(False)
                                        print("now you can see your led, ", is_it_truly_us)
                                        time.sleep(10) # Sleep for 1 second
                                       
                                    elif("onur" in is_it_truly_us):
                                        time.sleep(1) # Sleep for 1 second
                                        GPIO.setwarnings(False) # Ignore warning for now
                                        GPIO.cleanup()
                                        time.sleep(1) # Sleep for 1 second
                                        GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
                                        GPIO.setup(GPIO_LED1, GPIO.OUT, initial=GPIO.LOW) # Set pin 8 to be an output pin and >
                                        GPIO.output(GPIO_LED1, GPIO.HIGH) # Turn on
                                        
                                    
                                        
                                        time.sleep(1) # Sleep for 1 second
                                        GPIO.setup(GPIO_LED2, GPIO.OUT, initial=GPIO.LOW) # Set pin 8 to be an output pin and >
                                        GPIO.output(GPIO_LED2, GPIO.HIGH) # Turn on
                                        print("now you can see your led, ", is_it_truly_us)
                                        GPIO.setwarnings(False)
                                        time.sleep(10) # Sleep for 1 second
                                else:
                                    print("wrong PASSWORD , it was password ")  
                            except Exception as e:
                                print("this expect is !!!",e)
                        else:
                            print("I do not know you , you have not been registered")
                            GPIO.cleanup()
                    except Exception as e:
                        print("expection is ....", e)
                            
                except:
                    print("Network error")
    except KeyboardInterrupt:
        GPIO.cleanup()
        picam2.close()
        print("Measurement stopped by User")
        
