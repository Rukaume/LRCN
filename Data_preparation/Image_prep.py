# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 22:15:37 2021

@author: Miyazaki Shinichi
This script is for making images from a video.

Functions of this script
1. video to image convert
2. thinning out 
3. image aug (pixel value adjust)
4. subcrop for mice chambers
5. color to gray convert
6. change image size 

input: video (.avi)

parameter: chamber_num, fps, image_size, adjust value

output: .jpg files 
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

def make_directories():
    os.makedirs("./subcropped", exist_ok = True)
    os.makedirs("./subcropped/ch1", exist_ok = True)
    os.makedirs("./subcropped/ch2", exist_ok = True)
    os.makedirs("./subcropped/ch3", exist_ok = True)
    os.makedirs("./subcropped/ch4", exist_ok = True)


def save_frame(videopath, chamber, per_fps, image_size, Gray, filename,adjust_num):
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
    if chamber in [1, 2, 3, 4]:
        os.makedirs("./subcropped", exist_ok = True)
        os.makedirs("./subcropped/ch{}".format(chamber), exist_ok = True)
        ch_num = chamber-1
        for frame_num in tqdm(frame_list):
            frame_num = int(frame_num)
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
            ret, frame = cap.read()
            if ret:
                subcrop_im = frame[ROI[ch_num][2]:ROI[ch_num][3],
                                   ROI[ch_num][0]:ROI[ch_num][1]]
                resized_im = cv2.resize(subcrop_im, image_size)
                if Gray == 0:
                    image = adjust(cv2.cvtColor(resized_im, cv2.COLOR_BGR2GRAY), 
                                   adjust_num, beta = 0.0)  
                    cv2.imwrite("./subcropped/ch{0}/{1}.jpg".format(str(chamber), 
                                                                    str(frame_num)),image)
                else:
                    data.append(resized_im)
                    cv2.imwrite("./subcropped/ch{0}/{1}.jpg".format(str(chamber),
                                                                    str(frame_num)),resized_im)
    else:
        make_directories()
        for frame_num in tqdm(frame_list):
            frame_num = int(frame_num)
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
            ret, frame = cap.read()
            if ret:
                for i in range(len(ROI)):
                    ch_num = i + 1 
                    subcrop_im = frame[ROI[i][2]:ROI[i][3],ROI[i][0]:ROI[i][1]]
                    resized_im = cv2.resize(subcrop_im, image_size)
                    if Gray == 0:
                        image = adjust(cv2.cvtColor(resized_im, cv2.COLOR_BGR2GRAY), 
                                       adjust_num, beta = 0.0)  
                        cv2.imwrite("./subcropped/ch{0}/{1}.jpg".format(ch_num, frame_num),
                                    image)
                    else:
                        data.append(resized_im)
                        cv2.imwrite("./subcropped/ch{0}/{1}.jpg".format(ch_num, frame_num),
                                    resized_im)


def main():
    videopath = file_select()
    filename = os.path.splitext(os.path.basename(videopath))[0]
    chamber = int(input("chamber num (0 is for all chambers): "))
    per_fps = int(input("input 1/fps,3fps = 10: "))
    image_size = input("imagesize: ").split(",")
    image_size = (int(image_size[0]),int(image_size[1]))
    Gray = int(input("gray = 0, color = 1: "))
    adjust_num = float(input("adjust value (if you want to make gray scale images, you can adjust pixel values): "))
    save_frame(videopath, chamber, per_fps, image_size, Gray, filename, adjust_num)


if __name__ == '__main__':
    main()
    
