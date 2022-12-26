#!/usr/bin/env python3

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


gi.require_version("Gst", "1.0")
gi.require_version("GstVideo", "1.0")
from gi.repository import Gst, GstVideo

tmp = None
framecount = 0

ccstring = 'I420'
fourcc = cv2.VideoWriter_fourcc(*ccstring)
out = cv2.VideoWriter(f'./res/down16x_I420.avi', fourcc, 15, (1000, 750), 0)
container = np.zeros((750, 1000), dtype=np.uint8)

def callback(appsink, user_data):
    """
    This function will be called in a separate thread when our appsink
    says there is data for us. user_data has to be defined
    when calling g_signal_connect. It can be used to pass objects etc.
    from your other function to the callback.
    """
    sample = appsink.emit("pull-sample")
    global framecount
    # global tmp,container
    caps = sample.get_caps()
    if sample:
        gst_buffer = sample.get_buffer()
        try:
            (ret, buffer_map) = gst_buffer.map(Gst.MapFlags.READ)
            ### User defined operations based on the buffermap
            # d = gst_buffer.extract_dup(0, gst_buffer.get_size())
            img = np.ndarray((3000, 4000), buffer=buffer_map.data, dtype=np.uint8)
            container=skimage.measure.block_reduce(img, (4,4), np.mean)
            #container = img[::4, ::4]
            # container=cv2.resize(img,[750,1000])
            container = container.astype(np.uint8)
            container = np.expand_dims(container, axis=2)
            # print(img.shape)
            # container = cv2.flip(container, 0)
            out.write(container)
            # filename=f'./channel0/{framecount}.png'
            # cv2.imwrite(filename, img)
            print(framecount)
            print(container.shape)
            # tmp=img
            framecount += 1
        except Exception as e:
            print(e)

        finally:
            ## reload the buffer_map to the stream
            gst_buffer.unmap(buffer_map)
            pass

    return Gst.FlowReturn.OK


Gst.init(sys.argv)  # init gstreamer
Gst.debug_set_default_threshold(Gst.DebugLevel.WARNING)

serial = 17220805

pipeline = Gst.parse_launch("tcambin name=source"
                            " ! video/x-raw,format=GRAY8,width=4000,height=3000,framerate=15/1"
                            " ! videoconvert"
                            " ! appsink name=sink")
# test for error
if not pipeline:
    print("Could not create pipeline.")
    sys.exit(1)

# The user has not given a serial, so we prompt for one
if serial is not None:
    source = pipeline.get_by_name("source")
    source.set_property("serial", serial)

sink = pipeline.get_by_name("sink")

# tell appsink to notify us when it receives an image
sink.set_property("emit-signals", True)

user_data = "This is our user data"

# tell appsink what function to call when it notifies us
sink.connect("new-sample", callback, user_data)

pipeline.set_state(Gst.State.PLAYING)

print("Press Ctrl-C to stop.")

# We wait with this thread until a
# KeyboardInterrupt in the form of a Ctrl-C
# arrives. This will cause the pipline
# to be set to state NULL

time.sleep(10)

pipeline.set_state(Gst.State.NULL)
out2.release()