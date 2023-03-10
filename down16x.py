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
parser=argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-fname', type=str, default='test', help='file name (without extension)')
parser.add_argument('-delay', type=int, default=5, help='waitting time till starting to record')
parser.add_argument('-len', type=int, default=5, help='record length')
parser.add_argument('-serial', type=int, default=0, help='camera serial number')
parser = parser.parse_args()
gi.require_version("Gst", "1.0")
gi.require_version("GstVideo", "1.0")
from gi.repository import Gst, GstVideo
serial = parser.serial
tmp = None
framecount = 0
ccstring = 'I420'
fourcc = cv2.VideoWriter_fourcc(*ccstring)
file_location = f"./res/{parser.fname}.avi"



out = cv2.VideoWriter(file_location, fourcc, 15 , (1000, 750), 0)

container = np.zeros((750, 1000), dtype=np.uint8)


def callback(appsink, user_data):
    sample = appsink.emit("pull-sample")
    global framecount
    #caps = sample.get_caps()

def callback1(appsink, user_data):
    """
    This function will be called in a separate thread when our appsink
    says there is data for us. user_data has to be defined
    when calling g_signal_connect. It can be used to pass objects etc.
    from your other function to the callback.
    """
    sample = appsink.emit("pull-sample")
    global framecount
    #global tmp
    caps = sample.get_caps()
    if sample:
        gst_buffer = sample.get_buffer()
        try:
            (ret, buffer_map) = gst_buffer.map(Gst.MapFlags.READ)
            img = np.ndarray((3000, 4000), buffer=buffer_map.data, dtype=np.uint8)
            container=skimage.measure.block_reduce(img, (4,4), np.mean)
            container = container.astype(np.uint8)
            container = np.expand_dims(container, axis=2)
            out.write(container)
            #print(framecount)
            framecount += 1
        except Exception as e:
            print(e)
        finally:
            ## reload the buffer_map to the stream
            gst_buffer.unmap(buffer_map)
            pass
    return Gst.FlowReturn.OK


def callback2(appsink, user_data):
    """
    This function will be called in a separate thread when our appsink
    says there is data for us. user_data has to be defined
    when calling g_signal_connect. It can be used to pass objects etc.
    from your other function to the callback.
    """
    sample = appsink.emit("pull-sample")
    global framecount
    #global tmp
    caps = sample.get_caps()
    if sample:
        gst_buffer = sample.get_buffer()
        try:
            (ret, buffer_map) = gst_buffer.map(Gst.MapFlags.READ)
            img = np.ndarray((3000, 4000), buffer=buffer_map.data, dtype=np.uint8)
            container=skimage.measure.block_reduce(img, (4,4), np.mean)
            container = container.astype(np.uint8)
            #newbytes=container.tobytes('C')
            print(framecount)
            framecount += 1
        except Exception as e:
            print(e)
        finally:
            ## reload the buffer_map to the stream
            gst_buffer.unmap(Gst.Buffer.new_wrapped_bytes (container.tobytes('C')))
            pass
    return Gst.FlowReturn.OK



print(f'wait for {parser.delay} seconds')
time.sleep(parser.delay)
print(f'starting to record for {parser.len} seconds')
Gst.init()  # init gstreamer
Gst.debug_set_default_threshold(Gst.DebugLevel.WARNING)

pipeline = Gst.parse_launch("tcambin name=source"
                            " ! video/x-raw,format=GRAY8,width=4000,height=3000,framerate=15/1"
                            " ! videoconvert"
                            " ! appsink name=appsink"
                            #" ! filesink name=fsink"
                            )

if not pipeline:
    print("Could not create pipeline.")
    sys.exit(1)

if serial is not None:
    source = pipeline.get_by_name("source")
    source.set_property("serial", serial)

#file_location = f"./res/{parser.fname}.avi"
#fsink = pipeline.get_by_name("fsink")
#fsink.set_property("location", './res/hybrid.avi')

sink = pipeline.get_by_name("appsink")
sink.set_property("emit-signals", True)
user_data = None

# tell appsink what function to call when it notifies us
sink.connect("new-sample", callback1, user_data)

pipeline.set_state(Gst.State.PLAYING)

print("Press Ctrl-C to stop.")


time.sleep(parser.len)
pipeline.set_state(Gst.State.NULL)
out.release()

print('Recording finish')
print('total frame:',framecount)


