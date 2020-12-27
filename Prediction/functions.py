#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 12:35:35 2020

@author: miyazakishinichi

設計
連続するビデオデータを入力とする
numpyバイナリへの変換, モデルによる予測, 結果の出力
ジャンプの時間帯の抽出とビデオ化
可能であれば, 判断に迷った挙句に0にしたデータ群も
出力するデータは, 周囲も含めて出力することで, その時間帯の印象を見分けられるようにする
→ハードネガティブマイニング??
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
from tensorflow.keras.models import load_model
import time 
import pathlib
from skimage import io


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
    return len(roi_data)

def image_crop_and_prediction_wo_image_creation(ROI_file_path, Images_file_dir, image_size,
                              model, fps):
    Images_file_dir = pathlib.Path(Images_file_dir).resolve()
    os.chdir(Images_file_dir)
    imlist = os.listdir("./")
    roi_data = csv_file_read(ROI_file_path)
    roi_data['left'] = roi_data['BX']
    roi_data['right'] = roi_data['BX'] + roi_data['Width']
    roi_data['low'] = roi_data['BY']
    roi_data['high'] = roi_data['BY'] + roi_data['Height']
    
    roi = []
    X=[]
    image_size = tuple(image_size)
    model = model
    total_times = []
    result = []
    for i in range(len(roi_data)):
        num = i+1
        roi.append(roi_data.loc[num]['left':'high'])
        os.chdir(Images_file_dir)
        left, right, low, high = int(roi[i]['left']),\
                int(roi[i]['right']),int(roi[i]['low']),int(roi[i]['high'])
        data = [cv2.resize(cv2.imread(imlist[j],0)[low:high,left:right], 
                           image_size) for j in tqdm(range(len(imlist)))]
        X = np.asarray(data)
        X = X.astype('float32')
        X = X / 255.0
        X = np.expand_dims(X, 1)
        X = np.expand_dims(X, 4)
        predict_value  = pd.DataFrame(model.predict(X), columns = [0,1])
        predict_value["label"] = predict_value[0] - predict_value[1]
        predict_value["label"] = predict_value["label"] < 0
        predict_value["label"] = predict_value["label"].astype(int)
        #predict_classes = model.predict_classes(X)
        predict_classes = predict_value["label"].values
        result.append(predict_classes)
        total_time = predict_classes.sum()/fps
        total_times.append(total_time)
        os.chdir("../")
        np.savetxt("./ROI{}.csv".format(num), predict_classes, delimiter=",")
        np.savetxt("./ROI{}value.csv".format(num), predict_value, delimiter=",")
    return total_times, result

def image_crop_and_prediction(ROI_file_path, Images_file_dir, image_size,
                              model,fps):
    Images_file_dir = pathlib.Path(Images_file_dir).resolve()
    os.chdir(Images_file_dir)
    imlist = os.listdir("./")
    roi_data = csv_file_read(ROI_file_path)
    roi_data['left'] = roi_data['BX']
    roi_data['right'] = roi_data['BX'] + roi_data['Width']
    roi_data['low'] = roi_data['BY']
    roi_data['high'] = roi_data['BY'] + roi_data['Height']
    
    roi = []
    X=[]
    image_size = tuple(image_size)
    model = model
    total_times = []
    for i in range(len(roi_data)):
        num = i+1
        roi.append(roi_data.loc[num]['left':'high'])
        os.chdir(Images_file_dir)
        os.makedirs("../ROI{}".format(num), exist_ok = True)
        left, right, low, high = int(roi[i]['left']),\
                int(roi[i]['right']),int(roi[i]['low']),int(roi[i]['high'])
        data = []
        for j in tqdm(range(len(imlist))):
            tempimage = cv2.imread(imlist[j])
            subimage = tempimage[low:high,left:right]
            data.append(cv2.resize(subimage, image_size))
        X = np.asarray(data)
        X = X.astype('float32')
        X = X / 255.0
        X = np.expand_dims(X, 1)
        predict_classes = model.predict_classes(X)
        total_time = predict_classes.sum()/fps
        total_times.append(total_time)
        predict_value  = model.predict(X)
        os.chdir("../")
        np.savetxt("./ROI{}.csv".format(num), predict_classes, delimiter=",")
        np.savetxt("./ROI{}value.csv".format(num), predict_value, delimiter=",")
    return total_times

def save_all_frames(video_path, dir_path, basename,step, ext='jpg', num = 0):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return
    os.makedirs(dir_path, exist_ok=True)
    base_path = os.path.join(dir_path, basename)
    digit = len(str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))
    frame_num = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    print(frame_num)
    for i in tqdm(range(0, int(frame_num), int(step))):
        ret, frame = cap.read()
        cv2.imwrite('{}_{}.{}'.format(base_path, str(i).zfill(digit), ext), frame)


def prediction(data_dir, model, image_size, suffix):
    X = []
    image_size = tuple(image_size)
    model = model
    
    os.chdir(data_dir)
    dir_list = os.listdir("./")
    #exclude non-image files
    image_name_list = [i for i in dir_list if os.path.splitext(i)[1] == '.jpg']
    data = [cv2.resize(cv2.imread(image_name_list[j]), image_size) \
            for j in tqdm(range(len(image_name_list)))]

    X = np.asarray(data)
    X = X.astype('float32')
    X = X / 255.0
    X = np.expand_dims(X, 1)
    predict_classes = model.predict_classes(X)
    total_time = predict_classes.sum()
    predict_value  = model.predict(X)
    os.chdir("../")
    np.savetxt("./{}.csv".format(suffix), predict_classes, delimiter=",")
    np.savetxt("./{}value.csv".format(suffix), predict_value, delimiter=",")
    return total_time
