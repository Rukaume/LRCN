# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 22:27:11 2020

@author: Miyazaki
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
    messagebox.showinfo('cancel', 'stop before image_load')
    sys.exit()

imdir = os.path.dirname(image_file_path)

messagebox.showinfo('selectfiles', 'select result csvfile')
result_file_path = tkinter.filedialog.askopenfilename(initialdir = dir)



import os, cv2, shutil
from tqdm import tqdm
import pandas as pd 

result = pd.read_csv(result_file_path, usecols =["ROI1", "ROI2", "ROI3", "ROI4"])
result = result.values

os.chdir(imdir)
os.makedirs("../annotatedimages", exist_ok = True)

imlist =  os.listdir("./")
imlist = [i for i in imlist if os.path.splitext(i)[1] == '.jpg' \
                or os.path.splitext(i)[1] == '.png']
imlist.sort()

for i in tqdm(range(len(imlist))):
    im = cv2.imread(imlist[i])
    if int(result[i][0]) == 1:
        im = cv2.circle(im, (20, 20), 20, (255, 0, 0), 5, 8)
    else:
        pass
    if int(result[i][1]) == 1:
        im = cv2.circle(im, (340, 20), 20, (255, 0, 0), 5, 8)
    else:
        pass
    if int(result[i][2]) == 1:
        im = cv2.circle(im, (20, 260), 20, (255, 0, 0), 5, 8)
    else:
        pass
    if int(result[i][3]) == 1:
        im = cv2.circle(im, (340, 260), 20, (255, 0, 0), 5, 8)
    else:
        pass
    cv2.imwrite("../annotatedimages/{}".format(imlist[i]), im)
