# author: Qizhou Wang
# datetime: 1/25/23 10:31 PM
# email: imjoewang@gmail.com
"""
This module extract hypercube from video and save as the tiff format (float64)
"""
import h5py
import subprocess, os
import skimage.measure
import TIS
import cv2
import gi
import sys
import numpy as np
import matplotlib.pyplot as plt
import time
import os
import argparse
from utils import Camera, mkdir

out_fps=2
num_channel=34
out_width=56
out_height=48
resdir='./res/Jan19'
video_source='Vid/Jan19_30fps.avi'
cam=Camera()
cap = cv2.VideoCapture(os.path.join(resdir,video_source))
if (cap.isOpened()== False):
  print("Error opening video stream or file")
raw_fps=cap.get(cv2.CAP_PROP_FPS)
f_count=0
out_count=0
fps_ratio=raw_fps/out_fps

img=np.empty((out_height,out_width,9))
cube=np.empty((out_height,out_width,num_channel))

def change_dtype(cube):
    return cube.astype(np.float32)
    #return cube.astype(np.float64)
    #return any customized dtype

for channel in range(num_channel):
    mkdir(os.path.join(resdir,f'Hyper/chan{channel}'))

while(cap.isOpened()):
    ret, frame = cap.read()
    if not ret:
        print('File ends')
        break
    else:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        f_count = f_count + 1
        print(f_count)
        if f_count % fps_ratio == 1:
            out_count=out_count+1
            img[...]=cam.transform(frame)
            cube[...]=cam.inverse(img)
            cube=change_dtype(cube)
            for c in range(num_channel):
                # define the tiff filename here
                filename=os.path.join(resdir,f'Hyper/chan{c}/{out_count}.tiff')
                cv2.imwrite(filename,cube[:,:,c])
            break

cap.release()
print(f'total read {f_count} frames')
print(f'total extract {out_count} frames')

