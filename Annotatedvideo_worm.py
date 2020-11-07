# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 22:27:11 2020

@author: Miyazaki
"""

imdir = "C:/Users/Miyazaki/Desktop/hayashi_lab/20200527_lethargus_analysis/renamed_pillar_chamber-N2/chamber3"
resultdir= "C:/Users/Miyazaki/Desktop/hayashi_lab/20200527_lethargus_analysis/renamed_pillar_chamber-N2/result0918.csv"
import os, cv2, shutil
from tqdm import tqdm
import pandas as pd


os.chdir(imdir)
os.makedirs("../annotatedimages", exist_ok = True)

imlist =  os.listdir("./")
imlist = [i for i in imlist if os.path.splitext(i)[1] == '.jpg' \
                or os.path.splitext(i)[1] == '.png']
imlist.sort()

result = pd.read_csv(resultdir)
font = cv2.FONT_HERSHEY_SIMPLEX
for i in tqdm(range(len(imlist))):
  if int(result.loc[i]) == 0:
    tempim = cv2.imread(imlist[i])
    tempim = cv2.putText(tempim,'quiescent',(10,500), font, 1,(255,0,0),2,cv2.LINE_AA)
    cv2.imwrite('../annotatedimages/{}'.format(imlist[i]), tempim)
  elif int(result.loc[i]) == 1:
    tempim = cv2.imread(imlist[i])
    tempim = cv2.putText(tempim,'dwell',(10,500), font, 1,(0,255,0),2,cv2.LINE_AA)
    cv2.imwrite('../annotatedimages/{}'.format(imlist[i]), tempim)
  elif int(result.loc[i]) == 2:
    tempim = cv2.imread(imlist[i])
    tempim = cv2.putText(tempim,'forward',(10,500), font, 1,(0,0,255),2,cv2.LINE_AA)
    cv2.imwrite('../annotatedimages/{}'.format(imlist[i]), tempim)
  elif int(result.loc[i]) == 3:
    tempim = cv2.imread(imlist[i])
    tempim = cv2.putText(tempim,'backward',(10,500), font, 1,(100,100,0),2,cv2.LINE_AA)
    cv2.imwrite('../annotatedimages/{}'.format(imlist[i]), tempim)
  else:
    pass
