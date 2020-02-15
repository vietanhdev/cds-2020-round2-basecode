#!/usr/bin/env python3

import sys
import cv2
import numpy as np
from primesense import openni2#, nite2
from primesense import _openni2 as c_api
import config as cf
import time
import threading
import global_storage as gs


class Camera(threading.Thread):
    """This thread initialize 2 other threads (rgb and depth grabbers)
    """

    def __init__(self):
        threading.Thread.__init__(self)

        # Init device
        openni2.initialize(cf.OPENNI_PATH) #
        self.device = openni2.Device.open_any()

    def run(self):

        # Init RGB thread
        rgb_grabber = RGBCamera(self.device)
        rgb_grabber.start()

        # Init depth thread
        depth_grabber = DepthCamera(self.device)
        depth_grabber.start()

        # Wait threads to exit
        rgb_grabber.join()
        depth_grabber.join()


class RGBCamera(threading.Thread):

    def __init__(self, device):
        threading.Thread.__init__(self)
        self.device = device
    def run(self):

        print("Start rgb image thread")

        # Start camera stream
        rgb_stream = self.device.create_color_stream()
        rgb_stream.set_video_mode(c_api.OniVideoMode(pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_RGB888, resolutionX=640, resolutionY=480, fps=30))
        rgb_stream.start()

        # Get image continuously
        while not gs.exit_signal:
            time.sleep(0.05)
            bgr   = np.fromstring(rgb_stream.read_frame().get_buffer_as_uint8(),dtype=np.uint8).reshape(480,640,3)
            gs.rgb_frames.put(bgr)


class DepthCamera(threading.Thread):

    def __init__(self, device):
        threading.Thread.__init__(self)
        self.device = device
    def run(self):

        print("Start depth image thread")

        # Start camera stream
        depth_stream = self.device.create_depth_stream()
        depth_stream.set_video_mode(c_api.OniVideoMode(pixelFormat = c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_100_UM, resolutionX = 320, resolutionY = 240, fps = 30))
        depth_stream.start()

        # Get image continuously
        while not gs.exit_signal:
            time.sleep(0.05)
            frame = depth_stream.read_frame()
            frame_data = frame.get_buffer_as_uint16()
            img = np.frombuffer(frame_data, dtype=np.uint16)
            img.shape = (240, 320)
            img = cv2.flip(img,1)
            gs.depth_frames.put(img)
