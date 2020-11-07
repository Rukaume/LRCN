#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 21:04:28 2020

@author: miyazakishinichi
"""


import cv2
import os

import pandas as pd
from tkinter import messagebox
from tkinter import filedialog
import tkinter 
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import os, sys, cv2
from tqdm import tqdm


def save_all_frames(video_path, dir_path, basename, ext='jpg'):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return

    os.makedirs(dir_path, exist_ok=True)
    base_path = os.path.join(dir_path, basename)

    digit = len(str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))

    n = 0

    while True:
        ret, frame = cap.read()
        if ret:
            cv2.imwrite('{}_{}.{}'.format(base_path, str(n).zfill(digit), ext), frame)
            n += 1
        else:
            return


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
os.makedirs("./images", exist_ok = True)

save_all_frames(path,
                './images', 'img')

