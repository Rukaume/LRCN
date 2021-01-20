#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 21:05:03 2020

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

def image_cropper(ROI_file_path, Images_file_dir):
    os.chdir(Images_file_dir)
    imlist = os.listdir("./")
    roi_data = csv_file_read(ROI_file_path)
    roi_data['left'] = roi_data['BX']
    roi_data['right'] = roi_data['BX'] + roi_data['Width']
    roi_data['low'] = roi_data['BY']
    roi_data['high'] = roi_data['BY'] + roi_data['Height']
    
    roi = []
    for i in range(len(roi_data)):
        num = i+1
        roi.append(roi_data.loc[num]['left':'high'])
        os.makedirs("../ROI{}".format(num), exist_ok = True)
        left, right, low, high = int(roi[i]['left']),\
                int(roi[i]['right']),int(roi[i]['low']),int(roi[i]['high'])
        for j in tqdm(range(len(imlist))):
            tempimage = cv2.imread(imlist[j])
            subimage = tempimage[low:high,left:right]
            cv2.imwrite("../ROI{0}/{1}.jpg".format(num,str(j).zfill(7)), subimage)


####Tk root generate####
root = tkinter.Tk()
root.withdraw()

####ROI setting####
messagebox.showinfo('selectfiles', 'select csvfile for ROI setting')
ROI_file_path = tkinter.filedialog.askopenfilename(initialdir = dir)
if ROI_file_path == "":
    messagebox.showinfo('cancel', 'stop before ROI setting')
    sys.exit()
    
messagebox.showinfo('selectfiles', 'select image files')
path = filedialog.askopenfilename()
if path != False:
    pass
else:
    messagebox.showinfo('quit', 'stop the script')
    sys.exit()
Images_file_dir = os.path.dirname(path)


image_cropper(ROI_file_path, Images_file_dir)