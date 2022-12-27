#!/usr/bin/python3

# Capture a JPEG while still running in the preview mode. When you
# capture to a file, the return value is the metadata for that image.
import numpy as np
import time
import requests as re
import json 
import base64
import matplotlib.image as mpimg
import time

from PIL import Image
#from picamera2 import Picamera2, Preview
import yaml

# Opencv DNN

    


ip = "172.22.5.242"

#picam2 = Picamera2()

#preview_config = picam2.create_preview_configuration(main={"size": (1920, 1080)})
#picam2.configure(preview_config)

#picam2.start_preview(Preview.QTGL)

#picam2.start()
time.sleep(2)
picture_index=0
while True:    
    #picam2.capture_file("tmp.jpg")
    time.sleep(2) 
    #class_ids_string=convertTuple(class_ids)
    #scores_string=convertTuple(scores)
    #bboxes_string=convertTuple(bboxes)
    #print("is string :  ",type(class_ids_string),class_ids_string,"scores ", scores," scores string ",scores_string)


    try:    
        print( re.post("http://"+ip+":5000/end_point_3", files={'sound': open('sound.wav', 'rb')}) ) 
        time.sleep(2) 
        #print( re.post("http://"+ip+":5000/end_point_1b", files={'image': open('doritos_man.jpg', 'rb')}) )     
        #returned_img= re.post("http://"+ip+":5000/end_point_1a", files={'image': open('tmp.jpg', 'rb')}) 
        """  file = open('encode.bin', 'rb')
        byte = file.read()
        file.close()
  
        decodeit = open(returned_img, 'wb')
        decodeit.write(base64.b64decode((byte)))
        decodeit.close()"""
        """  this_img_name= 'pics/tmp'+str(picture_index)+'.jpg'
        rimg.save(this_img_name)
        picture_index=picture_index+1"""
   
        picture_index+=1
        #print( re.post("http://"+ip+":5000/end_point_1b", files={'image': open('tmp.jpg', 'rb')}) ) 
        #print( re.post("http://"+ip+":5000/end_point_2", json={'class': class_ids_string}) )
        #print( re.post("http://"+ip+":5000/end_point_2", json={'class': id2}) )
        #print( re.post("http://"+ip+":5000/end_point_2", json={'class': id3}) )
       

    except Exception as e:
        print("Network Error: ",e) 
        
    


picam2.close()