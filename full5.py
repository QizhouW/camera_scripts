# author: Qizhou Wang
# datetime: 12/20/22 5:56 PM
# email: imjoewang@gmail.com
"""
This module records the full size video stream
"""
import subprocess, os
import TIS
import cv2
import gi
import json
import sys
import numpy as np
import matplotlib.pyplot as plt
import time
gi.require_version("Tcam", "1.0")
gi.require_version("Gst", "1.0")
gi.require_version("GLib", "2.0")
from gi.repository import Tcam, Gst, GLib
import argparse

##---------Set Params---------------
parser=argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-fname', type=str, default='test', help='file name (without extension)')
parser.add_argument('-delay', type=int, default=1, help='waitting time till starting to record')
parser.add_argument('-len', type=int, default=10, help='record length')
parser.add_argument('-serial', type=int, default=0, help='camera serial number')
parser = parser.parse_args()

print(f'wait for {parser.delay} seconds')
time.sleep(parser.delay)

##----------Init the streaming pipeline---------------
Gst.init()
Gst.debug_set_default_threshold(Gst.DebugLevel.WARNING)
serial = parser.serial
if serial==0:
    serial = 17220805  # Hardcoded Serial , only for Debug
pipeline = Gst.parse_launch("tcambin name=bin"
                            " ! video/x-raw,format=GRAY8,width=4000,height=3000,framerate=5/1"
                            " ! videoconvert"
                            " ! avimux"
                            " ! filesink name=fsink")
# If use x264 compression, add compression string " ! x264enc speed-preset=ultrafast tune=zerolatency byte-stream=true bitrate=9000 threads=32"


##-----------Aquire the camera and set properties---------------
camera = pipeline.get_by_name("bin")
camera.set_property("serial", serial)

camera.set_state(Gst.State.READY)
camera.set_tcam_enumeration("ExposureAuto", "Off")
camera.set_tcam_enumeration("GainAuto", "Off")

# Load paramters from the json file, which is recorded by tcam-capture
with open('./setup.json', 'r') as f:
    params = json.load(f)
camera.set_tcam_float("ExposureTime", params['ExposureTime'])
camera.set_tcam_float("BlackLevel", params['BlackLevel'])
camera.set_tcam_float("Gain", params['Gain'])
print('Exposure time:',camera.get_tcam_float("ExposureTime")/1000,'ms')
print('BlackLevel:',camera.get_tcam_float("BlackLevel"))
print('Gain:',camera.get_tcam_float("Gain"),'db')

##----------Specify the file location and connect the pipeline to camera-----

file_location = f"./res/{parser.fname}.avi"
fsink = pipeline.get_by_name("fsink")
fsink.set_property("location", file_location)

##----------Record---------------------------------
print(f'start to record for {parser.len} seconds')
pipeline.set_state(Gst.State.PLAYING)
time.sleep(parser.len)
pipeline.set_state(Gst.State.NULL)

print('Recording finish')
