#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 22:27:06 2020

@author: miyazakishinichi
設計
複数のビデオデータを入力とする
numpyバイナリへの変換, モデルによる予測, 結果の出力
ジャンプの時間帯の抽出とビデオ化
→ハードネガティブマイニング用にデータを抽出？？

11/04追記
現状ではvideoから分割した画像を生成しているが, これは必要ではないので, 
GUIで作成するかどうか選択できるようにする
加えてデータの読出し等の方法を検討すること (最速を目指すなら, ビデオからskimageで読み込んで,
                       読み込んだデータをnumpyとして扱って直接予測器にかけてしまうというところ)
(現状, 1時間程度のデータの解析に1時間程度かかっているので, 可能ならもっと高速にしたいところ)


"""

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
from tkinter import messagebox
from tkinter import filedialog
import tkinter 
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from tkinter.scrolledtext import ScrolledText
import sys, os
import time 
import pandas as pd
from functions import save_all_frames
from tqdm import tqdm
from functions import image_cropper, prediction, image_crop_and_prediction,image_crop_and_prediction_wo_image_creation
import datetime
import pathlib
from tensorflow.keras.models import load_model

main_win = tk.Tk()
main_win.title("For LRCN")
main_win.geometry("500x400")

#main frame
main_frm = tk.Frame(main_win)
main_frm.grid(column=0, row=0, sticky=tk.NSEW, padx=5, pady=10)

#stickyはスペースに余裕がある場合に引き延ばすのか、どこに配置するのか　NSEWは全体引き延ばし
#padx yは余白設定

#label and combobox
Crop_label = tk.Label(main_frm, text="Crop or not")
Crop_comb = ttk.Combobox(main_frm,
                           values=["Crop", "Already cropped"])

Size_label = tk.Label(main_frm, text="image size (x,y)")
step_label = tk.Label(main_frm, text="Please enter value A,\n FPS/A")

Image_create_label = tk.Label(main_frm, text="Subimage create or not")
Image_create_comb = ttk.Combobox(main_frm,
                           values=["Create", "Not"])



####askfolderボタン動作定義####
def ask_folder():
    global path, videonames
    path = tkinter.filedialog.askdirectory()
    videonames = []
    [videonames.append(i) for i in os.listdir(path) if os.path.splitext(i)[-1] == '.avi' \
            or os.path.splitext(i)[-1] == '.mp4']
    file_path.set(videonames)

file_path = tk.StringVar()
folder_label = tk.Label(main_frm, text="video")
folder_box = tk.Entry(main_frm, textvariable = file_path)
folder_btn = tk.Button(main_frm, text="select", command=ask_folder)

####modelボタン動作定義####
def ask_model():
    global modelpath
    modelpath = tkinter.filedialog.askopenfilename()
    model_name = os.path.basename(modelpath)
    model_path.set(model_name)

model_path = tk.StringVar()
file_label = tk.Label(main_frm, text="model")
file_box = tk.Entry(main_frm, textvariable = model_path)
file_btn = tk.Button(main_frm, text="select", command=ask_model)

###ROIボタン動作定義###
def ask_ROI():
    global ROIpath
    ROIpath = tkinter.filedialog.askopenfilename()
    ROI_name = os.path.basename(ROIpath)
    ROI_path.set(ROI_name)

ROI_path = tk.StringVar()
ROI_label = tk.Label(main_frm, text="ROI csv file")
ROI_box = tk.Entry(main_frm, textvariable = ROI_path)
ROI_btn = tk.Button(main_frm, text="select", command=ask_ROI)

###Set button###
def set_image_size():
    global image_size
    image_size = imagesize_entry.get()
    image_size = image_size.split(",")
    image_size = [int(i) for i in image_size]
imagesize_entry = tk.Entry(
    main_frm)
set_imagesize_btn = tk.Button(main_frm, text="set", command=set_image_size)

def set_step():
    global step
    step = step_entry.get()
    step = int(step)
step_entry = tk.Entry(
    main_frm)
set_btn = tk.Button(main_frm, text="set", command=set_step)



#実行時の動作

####実行ボタン動作定義####
def execute():
    import time 
    t1 = time.time() 
    os.chdir(path)
    model = load_model(modelpath)
    num = 0
    #Crop or not
    Crop_txt = Crop_comb.get()
    Image_create = Image_create_comb.get()
    fps = 30/step
    jump_time = []
    for i in tqdm(videonames):
        os.chdir(path)
        os.makedirs("./video{}".format(num+1), exist_ok = True)
        save_all_frames(i, "./video{}/images".format(num+1),"image",
                        step = step, ext='jpg', num = num)
        if Crop_txt == "Crop" and Image_create == "Not":
            total_time_list, result = image_crop_and_prediction_wo_image_creation(ROIpath, 
                                                        "./video{}/images".format(num+1),
                                                        image_size,model, fps)
            jump_time.append(total_time_list)
            result = pd.DataFrame(result, index = ["ROI1", "ROI2", "ROI3", "ROI4"]).T
            result.to_csv('./result.csv')
        elif Crop_txt == "Crop" and Image_create == "Create":
            total_time_list = image_crop_and_prediction(ROIpath, 
                                                        "./video{}/images".format(num+1),
                                                        image_size,model,fps)
            jump_time.append(total_time_list)
        elif Crop_txt == "Already cropped":
            total_time = prediction("./images", model,
                                    image_size, "result")
            jump_time.appned(total_time)
        else:
            pass
        num += 1
    
    t2 = time.time()
    elapsed_time = t2-t1
    os.chdir(path)
    time = datetime.datetime.now()
    print(f"経過時間：{elapsed_time}")
    print(modelpath)
    print(path)
    print(ROIpath)
    path_w = './readme.txt'
    contents = '\nanalyzed_date: {0}\n'\
        'elapsed time: {1}\n'\
            'model: {2}\n'\
                'videos: {3}'.format(time,elapsed_time,modelpath, videonames)
    with open(path_w, mode = "a") as f:
        f.write(contents)
    jump_data = pd.DataFrame(jump_time, columns=['ROI1', 'ROI2', 'ROI3', 'ROI4'])
    jump_data.to_csv("./jump_time.csv")
    main_win.quit()
    main_win.destroy()
    sys.exit()
    

app_btn = tk.Button(main_frm, text="execute", command = execute)

###button function###
def quit_analysis():
    main_win.quit()
    main_win.destroy()

quit_btn = tk.Button(main_frm, text="quit", command = quit_analysis)



#配置
Crop_label.grid(column = 0, row = 0)
Crop_comb.grid(column = 1, row = 0, sticky = tk.W, padx = 5)

folder_label.grid(column=0, row=1, pady=10)
folder_box.grid(column=1, row=1, sticky=tk.EW, padx=5)
folder_btn.grid(column=2, row=1)

file_label.grid(column=0, row=2, pady=10)
file_box.grid(column=1, row=2, sticky=tk.EW, padx=5)
file_btn.grid(column=2, row=2)

ROI_label.grid(column=0, row=3, pady=10)
ROI_box.grid(column=1, row=3, sticky=tk.EW, padx=5)
ROI_btn.grid(column=2, row=3)

Size_label.grid(column=0, row=4, pady=10)
imagesize_entry.grid(column=1, sticky=tk.EW, row=4)
set_imagesize_btn.grid(column = 2, row=4)

step_label.grid(column=0, row=5, pady=10)
step_entry.grid(column=1, sticky=tk.EW, row=5)
set_btn.grid(column=2, row=5)

app_btn.place(relx=0.3, rely=0.9)
quit_btn.place(relx= 0.7,rely = 0.9)

Image_create_label.grid(column = 0, row = 6)
Image_create_comb.grid(column = 1, row = 6, sticky = tk.W, padx = 5)


main_win.columnconfigure(0, weight=1)
main_win.rowconfigure(0, weight=1)
main_frm.columnconfigure(1, weight=1)

main_win.mainloop()
sys.exit()