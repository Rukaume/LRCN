# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 09:30:18 2020

@author: miyas
This script is for converting Images to Numpy binary file.
"""
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
image_file_path = tkinter.filedialog.askopenfilename(initialdir = dir)
if image_file_path == "":
    messagebox.showinfo('cancel', 'stop before ROI setting')
    sys.exit()

imagedir = os.path.dirname(image_file_path)


num = int(input('please input image num'))
image_size = tuple([int(i) for i in \
                    input("コンマ区切りで画像サイズを指定 (横,縦)の順で").split(",")])

#suffix = str(input('please input suffix'))


import numpy as np 
import os, cv2
from tqdm import tqdm

#set image directory 

os.chdir(imagedir)
dirname = os.path.split(imagedir)
dir_name_list = os.listdir("./")
#exclude non-image files
image_name_list = [i for i in dir_name_list if os.path.splitext(i)[1] == '.jpg'\
                   or os.path.splitext(i)[1] == '.png']


data = []


for j in tqdm(range(len(image_name_list))[0:num]):
    data.append(cv2.resize(cv2.imread(image_name_list[j],0), image_size))

data = np.asarray(data)
np.save("../{0}.npy".format(dirname[-1]), data)

