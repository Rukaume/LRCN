# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 22:15:37 2021

@author: Miyazaki Shinichi
This script is for preparing labeled data for LRCN training.
1. video to image 
2. thinning out 
3. image aug 
4. make npy file

input: video (.avi)

parameter: fps, image_size

output: .npy
"""

import os, sys
import numpy as np
import pandas as pd
from tkinter import messagebox
from tkinter import filedialog
import tkinter 
import matplotlib.pyplot as plt
from tqdm import tqdm
import cv2 

def file_select():
    root = tkinter.Tk()
    root.withdraw()
    path = filedialog.askopenfilename()
    if path != False:
        pass
    else:
        messagebox.showinfo('quit', 'stop the script')
        sys.exit()
    folderpath = os.path.dirname(path)
    os.chdir(folderpath)
    return path


def adjust(img, alpha=1.0, beta=0.0):
    # change pixel value
    dst = alpha * img + beta
    # change to uint8
    return np.clip(dst, 0, 255).astype(np.uint8)


def save_frame(videopath, chamber, per_fps, image_size, Gray, filename):
    cap = cv2.VideoCapture(videopath)
    #exception catch for file read 
    if not cap.isOpened():
        return
    #obtain frame count
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    frame_list = np.arange(frame_count)[::per_fps]
    #ROI inf
    ROI = [[0,320,0,240],[320,640,0,240],[0,320,240,480],[320,640,240,480]]
    #image extract and subcrop
    data = []
    for frame_num in tqdm(frame_list):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        ret, frame = cap.read()
        if ret:
            subcrop_im = frame[ROI[chamber][2]:ROI[chamber][3],ROI[chamber][0]:ROI[chamber][1]]
            resized_im = cv2.resize(subcrop_im, image_size)
            if Gray == 0:
                image = cv2.cvtColor(resized_im, cv2.COLOR_BGR2GRAY)
            data.append(image)
    data = np.asarray(data)
    np.save("./{0}.npy".format(filename), data)

def main():
    videopath = file_select()
    filename = os.path.splitext(os.path.basename(videopath))[0]
    chamber = int(input("which chamber")) - 1
    per_fps = int(input("input 1/fps,3fps = 10"))
    image_size = input("imagesize").split(",")
    image_size = (int(image_size[0]),int(image_size[1]))
    Gray = int(input("gray = 0, color = 1"))
    save_frame(videopath, chamber, per_fps, image_size, Gray, filename)

main()

if __name__ == '__main__':
    main()
    
