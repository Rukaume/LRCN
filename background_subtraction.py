# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 09:30:43 2020

@author: miyas
"""

import os, cv2
import sys
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from tkinter import filedialog
import tkinter 
from tkinter import messagebox
import os.path
import time 
import numpy as np
from tqdm import tqdm
import scipy.stats
import datetime
from skimage.morphology import medial_axis, skeletonize
import matplotlib.patches as patches
from skimage import measure
from skimage.measure import label, regionprops
from PIL import Image, ImageTk
from functions import make_background_and_subtracted_images

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

imlist = os.listdir("./")
images = [i for i in imlist if os.path.splitext(i)[1] == '.jpg']
make_background_and_subtracted_images(images)