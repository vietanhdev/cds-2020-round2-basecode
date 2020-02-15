#!/usr/bin/env python3

import Adafruit_PCA9685
import sys
import config as cf
import time
import threading
import global_storage as gs
import math
import time
usleep = lambda x: time.sleep(x/1000000.0)


class MotorController(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

        # Init controller
        self.pwm = Adafruit_PCA9685.PCA9685(address=0x40, busnum=1)
        self.pwm.set_pwm_freq(cf.MOTOR_FREQ)
        usleep(5000)

        # Reset state
        self.direction = 0
        pwm_steer_middle = self.value_map(0, cf.MIN_ANGLE, cf.MAX_ANGLE, cf.STEERING_MAX_RIGHT, cf.STEERING_MAX_LEFT)
        self.pwm.set_pwm(cf.STEERING_CHANNEL, 0, pwm_steer_middle)
        self.pwm.set_pwm(cf.THROTTLE_CHANNEL, 0, cf.THROTTLE_NEUTRAL)

    def run(self):
        while not gs.exit_signal:
            self.set_speed(gs.speed)
            self.set_steer(gs.steer)

    def set_speed(self, throttle_val):
        if throttle_val > 0:
            if self.direction == -1:
                self.pwm.set_pwm(cf.THROTTLE_CHANNEL, 0, cf.THROTTLE_MAX_FORWARD)
                usleep(187500)
                self.pwm.set_pwm(cf.THROTTLE_CHANNEL, 0, cf.THROTTLE_NEUTRAL)
                direction = 0
                usleep(187500)

            self.direction = 1
            pwm = self.value_map(throttle_val, 0, 100, cf.THROTTLE_NEUTRAL, cf.THROTTLE_MAX_FORWARD)
            self.pwm.set_pwm(cf.THROTTLE_CHANNEL, 0, pwm)
        elif throttle_val < 0:
            if self.direction == 1:
                self.pwm.set_pwm(cf.THROTTLE_CHANNEL, 0, cf.THROTTLE_MAX_REVERSE)
                usleep(187500)
                self.pwm.set_pwm(cf.THROTTLE_CHANNEL, 0, cf.THROTTLE_NEUTRAL)
                direction = 0
                usleep(187500)
            self.direction = -1
            pwm = 4095 - self.value_map( abs(throttle_val), 0, 100 , 4095 - cf.THROTTLE_NEUTRAL , 4095 - cf.THROTTLE_MAX_REVERSE)
            self.pwm.set_pwm(cf.THROTTLE_CHANNEL, 0, pwm)
        usleep(5000)

    def set_steer(self, steer_angle):
        steer_angle =  min(cf.MAX_ANGLE, max(cf.MIN_ANGLE, steer_angle))
        pwm = self.value_map(steer_angle, cf.MIN_ANGLE, cf.MAX_ANGLE, cf.STEERING_MAX_RIGHT, cf.STEERING_MAX_LEFT)
        self.pwm.set_pwm(cf.STEERING_CHANNEL, 0, pwm)
        usleep(5000)
        
    def value_map (self, x, in_min, in_max, out_min, out_max):
        return int( 1.0 * (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min )




