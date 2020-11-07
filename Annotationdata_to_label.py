# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 17:40:10 2020

@author: Miyazaki
"""
import os 
import pandas as pd 
from tkinter import messagebox
from tkinter import filedialog
import tkinter 
import sys
import numpy as np

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

#read csv
data = pd.read_csv(path)
#reset indices
data = data.reset_index()
#extract start and end data 
startdata = data.iloc[:,2]
enddata = data.iloc[:,3]

#initialized array
label = np.zeros(18000)

#loop
#Is last data always nan??
for i in range(len(startdata)-1):
    label[int(startdata[i]):int(enddata[i])] = 1
    
#save as csv
np.savetxt("./label.csv", label, delimiter =",")
