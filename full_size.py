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
import sys
import numpy as np
import matplotlib.pyplot as plt
import time
gi.require_version("Tcam", "1.0")
gi.require_version("Gst", "1.0")
from gi.repository import Tcam, Gst
import argparse
parser=argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('-fname', type=str, default='test', help='file name (without extension)')
parser.add_argument('-delay', type=int, default=10, help='waitting time till starting to record')
parser.add_argument('-len', type=int, default=10, help='record length')

parser = parser.parse_args()
print(f'wait for {parser.delay} seconds')
time.sleep(parser.delay)
print(f'starting to record for {parser.len} seconds')
Gst.init() 
Gst.debug_set_default_threshold(Gst.DebugLevel.WARNING)
serial = 17220805
pipeline = Gst.parse_launch("tcambin name=bin"
                            " ! video/x-raw,format=GRAY8,width=4000,height=3000,framerate=30/1"
                            " ! videoconvert"
                            #" ! x264enc speed-preset=ultrafast tune=zerolatency byte-stream=true bitrate=9000 threads=32"
                            " ! avimux"
                            " ! filesink name=fsink")

if serial is not None:
    camera = pipeline.get_by_name("bin")
    camera.set_property("serial", serial)

file_location = f"./res/{parser.fname}.avi"

fsink = pipeline.get_by_name("fsink")
fsink.set_property("location", file_location)

pipeline.set_state(Gst.State.PLAYING)
time.sleep(parser.len)
pipeline.set_state(Gst.State.NULL)

print('Recording finish')
