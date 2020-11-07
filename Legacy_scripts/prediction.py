# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 19:39:56 2020

@author: Miyazaki
"""

import os, cv2
import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as pat
from tkinter import filedialog
import tkinter 
from tkinter import messagebox
import os.path
import time 
import numpy as np
from tqdm import tqdm
import scipy.stats
import datetime
from PIL import Image, ImageTk
from keras.models import load_model
from keras.preprocessing.image import img_to_array, load_img
from keras import backend as K 
from keras.preprocessing.image import array_to_img, img_to_array, load_img
from keras.preprocessing.image import array_to_img, img_to_array, load_img
import cv2
import os
import re
import keras

####Tk root generate####
root = tkinter.Tk()
root.withdraw()

####file select & directory setting####
path = filedialog.askopenfilename()
if path != False:
    pass
else:
    messagebox.showinfo('quit', 'stop the script')
    sys.exit()
folderpath = os.path.dirname(path)
os.chdir(folderpath)

model = load_model(path, compile=False)

datapath = filedialog.askopenfilename()
datapath = os.path.dirname(datapath)
if path != False:
    pass
else:
    messagebox.showinfo('quit', 'stop the script')
    sys.exit()

def list_pictures(directory, ext='jpg|jpeg|bmp|png|ppm'):
    return [os.path.join(root, f)
            for root, _, files in os.walk(directory) for f in files
            if re.match(r'([\w]+\.(?:' + ext + '))', f.lower())]

X = []
os.chdir(datapath)
for picture in tqdm(list_pictures("./")[0:999]):
    img = img_to_array(load_img(picture, target_size=(80, 120)))
    X.append(img)

X = np.asarray(X)
X = X.astype('float32')
X = X / 255.0
X = np.expand_dims(X, 1)

predict_classes = model.predict_classes(X)
os.chdir(folderpath)
np.savetxt("./result.csv", predict_classes, delimiter=",")