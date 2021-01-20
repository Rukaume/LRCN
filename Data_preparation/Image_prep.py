# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 22:15:37 2021

@author: Miyazaki Shinichi
1. Description 
This script is for making images from a video.

2. How to use 
    1. run this script
    2. select your video
    3. put the chamber number which you want to extract images. If you wanted to 
    extract from all of chambers, please put 0.
    4. put the value 1/fps. If your video's fps was about 30 and you wanted to 
    extract images every 1 minutes, please put 1800 (=30(fps)*60(sec)). 
    5. you can also select output image size. ex) 200,150
    6. you can choose gray scale or cololized
    7. If you selected gray, you can modify pixel values (for image augmentation)


input: video (.avi)
output: images (.jpg)  
"""

import os
import sys
import tkinter
from tkinter import filedialog, messagebox

import cv2
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm


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
    # make lookup table
    lut = alpha * np.arange(256, dtype= np.float64) + beta
    lut = np.clip(lut, 0, 255).astype(np.uint8)
    return cv2.LUT(img, lut)


def make_directories():
    os.makedirs("./extracted", exist_ok=True)
    os.makedirs("./extracted/ch1", exist_ok=True)
    os.makedirs("./extracted/ch2", exist_ok=True)
    os.makedirs("./extracted/ch3", exist_ok=True)
    os.makedirs("./extracted/ch4", exist_ok=True)


def save_frame(videopath, chamber, per_fps, image_size, Gray, filename, adjust_num):
    cap = cv2.VideoCapture(videopath)
    # exception catch for file read
    if not cap.isOpened():
        return
    # obtain frame count
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    frame_list = np.arange(0, frame_count, per_fps, dtype=int)
    # ROI inf
    # {chamber: (x1, x2, y1, y2)}
    ROI = {
        1: (0, 320, 0, 240),
        2: (320, 640, 0, 240),
        3: (0, 320, 240, 480),
        4: (320, 640, 240, 480)
    }
    # image extract and subcrop
    data = []
    if chamber in ROI:
        os.makedirs("./extracted", exist_ok=True)
        os.makedirs("./extracted/ch{}".format(chamber), exist_ok=True)
        for frame_num in tqdm(frame_list):
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
            ret, frame = cap.read()
            if ret:
                x1, x2, y1, y2 = ROI[chamber]
                subcrop_im = frame[y1:y2, x1:x2]
                resized_im = cv2.resize(subcrop_im, image_size)
                if Gray == 0:
                    image = adjust(cv2.cvtColor(resized_im, cv2.COLOR_BGR2GRAY),
                                   adjust_num, beta=0.0)
                    cv2.imwrite("./extracted/ch{0}/{1}.jpg".format(str(chamber),
                                                                    str(frame_num)), image)
                else:
                    data.append(resized_im)
                    cv2.imwrite("./extracted/ch{0}/{1}.jpg".format(str(chamber),
                                                                    str(frame_num)), resized_im)
    else:
        make_directories()
        for frame_num in tqdm(frame_list):
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
            ret, frame = cap.read()
            if ret:
                for chamber, (x1, x2, y1, y2) in ROI.items():
                    subcrop_im = frame[y1:y2, x1:x2]
                    resized_im = cv2.resize(subcrop_im, image_size)
                    if Gray == 0:
                        image = adjust(cv2.cvtColor(resized_im, cv2.COLOR_BGR2GRAY),
                                       adjust_num, beta=0.0)
                        cv2.imwrite("./extracted/ch{0}/{1}.jpg".format(chamber, frame_num),
                                    image)
                    else:
                        data.append(resized_im)
                        cv2.imwrite("./extracted/ch{0}/{1}.jpg".format(chamber, frame_num),
                                    resized_im)


def main():
    videopath = file_select()
    filename = os.path.splitext(os.path.basename(videopath))[0]
    print("Please specify the output parameters...")
    chamber = int(input("chamber num (0 is for all chambers): "))
    per_fps = int(input("input 1/fps, 3fps = 10: "))
    image_size = input(
        "imagesize('width, height', ex: '320,240'): ").split(",")
    image_size = tuple(map(int, image_size))
    Gray = int(input("gray = 0, color = 1: "))
    adjust_num = float(input(
        "adjust value (if you want to make gray scale images,\n you can adjust pixel values): "))
    print("Start Process...")
    save_frame(videopath, chamber, per_fps,
               image_size, Gray, filename, adjust_num)


if __name__ == '__main__':
    main()
