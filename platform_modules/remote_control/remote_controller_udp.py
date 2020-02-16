#!/usr/bin/env python3
import sys
import config as cf
import time
import threading
import global_storage as gs
import signal
import os
import json
import socket

localIP     = "0.0.0.0"
localPort   = 12345
bufferSize  = 1024

class RemoteControllerUDP(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

        # Create a datagram socket
        self.UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        
        # Bind to address and ip
        self.UDPServerSocket.bind((localIP, localPort))


    def run(self):
        
        # Listen for incoming datagrams
        while(True):

            bytesAddressPair = self.UDPServerSocket.recvfrom(bufferSize)
            message = bytesAddressPair[0]
            # address = bytesAddressPair[1]
            message = message.decode("ascii")

            x1 = int(message[:4])
            y1 = int(message[4:8])
            x2 = int(message[8:12])
            y2 = int(message[12:])

            
            gs.remote_control_speed = (1500-y1) / 500.0 
            gs.remote_control_steer_angle = (1500-x2) / 500.0
            gs.speed = min(gs.remote_control_speed * cf.MAX_SPEED, cf.MAX_SPEED)
            gs.steer = max(min(gs.remote_control_steer_angle * cf.MIN_ANGLE, cf.MAX_ANGLE), cf.MIN_ANGLE)
            # gs.record_videos = control_params["record_videos"]
            # if control_params["emergency_stop"]:
            #     gs.emergency_stop = control_params["emergency_stop"]
            gs.last_time_control_signal = time.time()

           


