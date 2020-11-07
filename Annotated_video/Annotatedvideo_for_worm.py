# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 17:10:22 2020

@author: miyas
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
image_file_path = tkinter.filedialog.askopenfilename()
if image_file_path == "":
    messagebox.showinfo('cancel', 'stop before setting')
    sys.exit()

imdir = os.path.dirname(image_file_path)

messagebox.showinfo('selectfiles', 'select result file ')
resultdir= tkinter.filedialog.askopenfilename()

result = pd.read_csv(resultdir)

os.chdir(imdir)
os.makedirs("../annotatedimages", exist_ok = True)

imlist =  os.listdir("./")
imlist = [i for i in imlist if os.path.splitext(i)[1] == '.jpg' \
                or os.path.splitext(i)[1] == '.png']
imlist.sort()
for i in tqdm(range(len(imlist))):
    im = cv2.imread(imlist[i])
    if int(result.loc[i]) ==0 :
        im = cv2.putText(im, "quiescent", (150, 100),
                         cv2.FONT_HERSHEY_SIMPLEX,0.7,
                         color = (255,0,0))
    elif int(result.loc[i]) == 1:
        im = cv2.putText(im, "dwelling", (150, 100),
                         cv2.FONT_HERSHEY_SIMPLEX,0.7,
                         color = (0,255,0))
    elif int(result.loc[i]) == 2:
        im = cv2.putText(im, "forward", (150, 100),
                         cv2.FONT_HERSHEY_SIMPLEX,0.7,
                         color = (0,0,255))
    elif int(result.loc[i]) == 3:
        im = cv2.putText(im, "backward", (150, 100),
                         cv2.FONT_HERSHEY_SIMPLEX,0.7,
                         color = (100,100,100))
    else:
        pass
    cv2.imwrite("../annotatedimages/{}".format(imlist[i]), im)
