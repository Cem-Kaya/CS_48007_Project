# Authored by Cem Kaya & Emre can eski
import threading
import json
import codecs
from time import strptime
import requests as req
from flask import send_file
from flask_cors import CORS
from flask import Flask, render_template, request, send_from_directory, send_file
import torch 
import torchvision
import cv2
import numpy as np
import base64
from matplotlib import pyplot as plt
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import whisper

import matplotlib.image as mpimg

# py -3.10 .\back_end.py # to run the server
# py -3.10 -m pip freeze > requirements.txt # to create requirements.txt
# py -3.10 -m pip install -r requirements.txt # to install requirements.txt 
def results_parser(results):
  s = ""
  if results.pred[0].shape[0]:
    for c in results.pred[0][:, -1].unique():
      n = (results.pred[0][:, -1] == c).sum()  # detections per class
      s += f"{n} {results.names[int(c)]}{'s' * (n > 1)}, "  # add to string
  return s

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
  return render_template('index.html')


@app.route('/end_point_1a', methods=['POST'], strict_slashes=False  )
def end_point_1a():
    global picture_index
    file = request.files['image']

    this_img_name= 'tmp'+'.jpg'
    file.save(this_img_name)
   
    
    
    #results.save()
    
    
   
    return "true" 

@app.route('/end_point_3', methods=['POST'], strict_slashes=False  )
def end_point_3():
  print("first")
  file = request.files['sound']
  print("second")
  this_sound_name= 'sound'+'.wav'
  print("third")
  file.save(this_sound_name)
  print("fourth")
  model = whisper.load_model("base")
  
  # load audio and pad/trim it to fit 30 seconds
  audio = whisper.load_audio("sound.wav")
  audio = whisper.pad_or_trim(audio)

# make log-Mel spectrogram and move to the same device as the model
  mel = whisper.log_mel_spectrogram(audio).to(model.device)

# detect the spoken language
  _, probs = model.detect_language(mel)
  print(f"Detected language: {max(probs, key=probs.get)}")

# decode the audio
  options = whisper.DecodingOptions(fp16 = False)
  result = whisper.decode(model, mel, options)

# print the recognized text
  print(result.text)
  print("accepted")
  return "accepted"
  
  
    
    
    






#################################################
if __name__ == '__main__':  #python interpreter assigns "__main__" to the file you run
    app.run(debug=False , host="172.22.5.242")