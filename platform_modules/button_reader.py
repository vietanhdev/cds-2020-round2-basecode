#!/usr/bin/env python3
import gpio
import sys
import config as cf
import time
import threading
import global_storage as gs
import signal

class ButtonReader(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        gpio.setup(cf.GPIO_BUTTON_1, gpio.IN)
        gpio.setup(cf.GPIO_BUTTON_2, gpio.IN)
        gpio.setup(cf.GPIO_BUTTON_3, gpio.IN)
        gpio.setup(cf.GPIO_BUTTON_4, gpio.IN)
        gpio.setup(cf.GPIO_BUTTON_SS1, gpio.IN)
        gpio.setup(cf.GPIO_BUTTON_SS2, gpio.IN)

        # Exit signal handle
        signal.signal(signal.SIGUSR2, self.clean_up_gpio)
        signal.signal(signal.SIGTERM, self.clean_up_gpio)
        signal.signal(signal.SIGINT, self.clean_up_gpio)
        

    def run(self):
        while not gs.exit_signal:
            gs.button_1 = gpio.read(cf.GPIO_BUTTON_1)
            gs.button_2 = gpio.read(cf.GPIO_BUTTON_2)
            gs.button_3 = gpio.read(cf.GPIO_BUTTON_3)
            gs.button_4 = gpio.read(cf.GPIO_BUTTON_4)
            gs.button_ss1 = gpio.read(cf.GPIO_BUTTON_SS1)
            gs.button_ss2 = gpio.read(cf.GPIO_BUTTON_SS2)
            time.sleep(0.05)

    def clean_up_gpio(self, num, stack):
        print("Clean up GPIO...")
        gpio.cleanup(cf.GPIO_BUTTON_1)
        gpio.cleanup(cf.GPIO_BUTTON_2)
        gpio.cleanup(cf.GPIO_BUTTON_3)
        gpio.cleanup(cf.GPIO_BUTTON_4)
        gpio.cleanup(cf.GPIO_BUTTON_SS1)
        gpio.cleanup(cf.GPIO_BUTTON_SS2)
        exit(0)