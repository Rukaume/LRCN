#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 21:19:37 2020

@author: miyazakishinichi
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

def csv_file_read(filepath):
    file_dir, file_name = os.path.split(filepath)
    base, ext = os.path.splitext(file_name)
    if ext == '.csv':
        data = pd.read_csv(filepath, index_col = 0)
        return data
    else:
        return messagebox.showinfo('error',
                            'selected file is not csv file')
    


####Tk root generate####
root = tkinter.Tk()
root.withdraw()

####ROI setting####
messagebox.showinfo('selectfiles', 'select csvfile for ROI setting')
ROI_file_path = tkinter.filedialog.askopenfilename(initialdir = dir)
if ROI_file_path == "":
    messagebox.showinfo('cancel', 'stop before ROI setting')
    sys.exit()

roi_data = csv_file_read(ROI_file_path)
roi_data['left'] = roi_data['BX']
roi_data['right'] = roi_data['BX'] + roi_data['Width']
roi_data['low'] = roi_data['BY'] 
roi_data['high'] = roi_data['BY'] + roi_data['Height']

roi = roi_data.loc[4]['left':'high']

####file select & directory setting####
messagebox.showinfo('selectfiles', 'select image files')
path = filedialog.askopenfilename()
if path != False:
    pass
else:
    messagebox.showinfo('quit', 'stop the script')
    sys.exit()
folderpath = os.path.dirname(path)
os.chdir(folderpath)

imlist = os.listdir("./")
os.makedirs("../chamber1", exist_ok = True)

for i in tqdm(range(len(imlist))):
    tempimage = cv2.imread(imlist[i])
    left, right, low, high = int(roi['left']),\
            int(roi['right']),int(roi['low']),int(roi['high'])
    subimage = tempimage[low:high,left:right]
    cv2.imwrite("../chamber1/{}.jpg".format(str(i).zfill(5)), subimage)
    