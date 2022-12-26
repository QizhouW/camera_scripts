# author: Qizhou Wang
# datetime: 12/20/22 5:56 PM
# email: imjoewang@gmail.com
"""
This module
"""


#!/usr/bin/env python3

#
# This example will show you how to save a video stream to a file
#

import subprocess, os
script='tiscamera-env.sh'
pipe = subprocess.Popen(f"source ./{script}; env", stdout=subprocess.PIPE, shell=True)
output = pipe.communicate()[0]
# = dict((line.decode("utf-8").split("=", 1) for line in output.splitlines()))
#os.environ.update(env)
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

Gst.init(sys.argv)  # init gstreamer


# this line sets the gstreamer default logging level
# it can be removed in normal applications
# gstreamer logging can contain verry useful information
# when debugging your application
# see https://gstreamer.freedesktop.org/documentation/tutorials/basic/debugging-tools.html
# for further details
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

file_location = f"./{fname}.avi"

fsink = pipeline.get_by_name("fsink")
fsink.set_property("location", file_location)

pipeline.set_state(Gst.State.PLAYING)
time.sleep(record_time)

pipeline.set_state(Gst.State.NULL)


