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
import os
import pathlib
import logging
from utils.queue_handle import *

class Camera(threading.Thread):
    """This thread initialize 2 other threads (rgb and depth grabbers)
    """

    def __init__(self):
        threading.Thread.__init__(self)

        # Init device
        openni2.initialize(cf.OPENNI_PATH) #
        self.device = openni2.Device.open_any()

        self.record_videos = gs.record_videos

    def run(self):

        # Init RGB thread
        rgb_grabber = RGBCamera(self.device)
        rgb_grabber.start()

        # Init depth thread
        depth_grabber = DepthCamera(self.device)
        depth_grabber.start()

        while not gs.exit_signal:
            time.sleep(1)
            if self.record_videos != gs.record_videos:
                if gs.record_videos: # Turn on video recording

                    print("Start recording...")

                    gs.is_recording = False

                    folder_name = time.strftime("%Y%m%d-%H%M%S")

                    video_folder = os.path.join(cf.RECORDING_PATH, folder_name)
                    pathlib.Path(video_folder).mkdir(parents=True, exist_ok=True)

                    gs.rgb_video_file = os.path.join(video_folder, "rgb_" + folder_name + ".avi")
                    gs.depth_video_file = os.path.join(video_folder, "depth_" + folder_name + ".avi")

                    gs.rgb_frame_count = 0

                    gs.is_recording = True

                    rgb_grabber.start_recording(gs.rgb_video_file)
                    # depth_grabber.start_recording(gs.depth_video_file)

                else: # Stop video recording

                    print("Stop recording...")

                    rgb_grabber.stop_recording()
                    # depth_grabber.stop_recording()

                self.record_videos = gs.record_videos


        # Wait threads to exit
        rgb_grabber.join()
        depth_grabber.join()

        print("Camera thread")


class RGBCamera(threading.Thread):

    out_file = None
    is_recording = False

    def __init__(self, device):
        threading.Thread.__init__(self)
        self.device = device

    def run(self):

        # create logger with 'rgb_camera'
        logger = logging.getLogger('rgb_camera')
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler('rgb_camera.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        logger.debug("Start rgb image thread")

        # Start camera stream
        rgb_stream = self.device.create_color_stream()
        rgb_stream.set_video_mode(c_api.OniVideoMode(pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_RGB888, resolutionX=320, resolutionY=240, fps=30))
        rgb_stream.start()

        # Get image continuously
        while not gs.exit_signal:
            img = np.fromstring(rgb_stream.read_frame().get_buffer_as_uint8(),dtype=np.uint8).reshape(240,320,3)
            bgr   = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

            put_to_queue_no_wait_no_block(bgr, gs.rgb_frames)
            
            if RGBCamera.is_recording:
                RGBCamera.out_file.write(bgr)


        logger.debug("Exiting from RGB image grabber")

    def start_recording(self, file_path):
        if RGBCamera.out_file is not None:
            self.stop_recording()
        
        fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        RGBCamera.out_file = cv2.VideoWriter(file_path, fourcc, 20.0, (320,240))

        RGBCamera.is_recording = True

    def stop_recording(self):
        if RGBCamera.out_file is not None:
            try:
                RGBCamera.out_file.release()
            except e:
                print(e)
        RGBCamera.is_recording = False


class DepthCamera(threading.Thread):

    out_file = None
    is_recording = False

    def __init__(self, device):
        threading.Thread.__init__(self)
        self.device = device
        self.out_file = None
    def run(self):

        print("Start depth image thread")

        # Start camera stream
        depth_stream = self.device.create_depth_stream()
        depth_stream.set_video_mode(c_api.OniVideoMode(pixelFormat = c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_100_UM, resolutionX = 320, resolutionY = 240, fps = 30))
        depth_stream.start()

        # Get image continuously
        while not gs.exit_signal:
            frame = depth_stream.read_frame()
            frame_data = frame.get_buffer_as_uint16()
            img = np.frombuffer(frame_data, dtype=np.uint16)
            img.shape = (240, 320)
            img = cv2.flip(img,1)

            put_to_queue_no_wait_no_block(img, gs.depth_frames)
            
            if DepthCamera.is_recording:
                img_rgb = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
                cvuint8 = cv2.convertScaleAbs(img_rgb)
                DepthCamera.out_file.write(cvuint8)


        print("Exiting from Depth image grabber")

    def start_recording(self, file_path):
        if DepthCamera.is_recording:
            self.stop_recording()
        
        fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        DepthCamera.out_file = cv2.VideoWriter(file_path, fourcc, 20.0, (320, 240))

        DepthCamera.is_recording = True

    def stop_recording(self):
        if DepthCamera.is_recording:
            try:
                DepthCamera.out_file.release()
            except e:
                print(e)
        DepthCamera.is_recording = False