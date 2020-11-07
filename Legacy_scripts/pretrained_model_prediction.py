a# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 16:06:15 2020

@author: miyas
"""

import json
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import array_to_img, img_to_array, load_img
import cv2
import os
import re
from tqdm import tqdm

import pandas as pd
from tkinter import messagebox
from tkinter import filedialog
import tkinter 
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import os, sys, cv2
from tqdm import tqdm



####Tk root generate####
root = tkinter.Tk()
root.withdraw()

####ROI setting####
messagebox.showinfo('selectfiles', 'select imagefiles')
image_file_path = tkinter.filedialog.askopenfilename()
if image_file_path == "":
    messagebox.showinfo('cancel', 'stop before setting')
    sys.exit()

data_dir = os.path.dirname(image_file_path)

messagebox.showinfo('selectfiles', 'select model')
model_dir = tkinter.filedialog.askopenfilename()

X = []
os.chdir(data_dir)
dir_name_list = os.listdir("./")
#exclude non-image files
image_name_list = [i for i in dir_name_list if os.path.splitext(i)[1] == '.jpg']
data = []
for j in tqdm(range(len(image_name_list))[0:3000]):

    data.append(cv2.resize(cv2.imread(image_name_list[j]), (100, 75)))


model = load_model(model_dir)   

X = np.asarray(data)
X = X.astype('float32')
#X = X[:,:,:,np.newaxis]
X = X / 255.0
X = np.expand_dims(X, 1)

predict_classes = model.predict_classes(X)
os.chdir(data_dir)
os.chdir("../")
np.savetxt("./result1005.csv", predict_classes, delimiter=",")

