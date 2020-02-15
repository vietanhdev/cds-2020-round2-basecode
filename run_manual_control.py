import signal
import sys
from platform_modules.motor_controller import MotorController
from platform_modules.lcd_driver import LCD
from platform_modules.button_reader import ButtonReader
from platform_modules.car_guard import CarGuard
from utils.keyboard_getch import _Getch
import global_storage as gs
import config as cf


# Init LCD
lcd = LCD(cf.LCD_ADDRESS)

# Init button reader
button_reader = ButtonReader()
button_reader.start()

# Init motor controller
mc = MotorController()
mc.start()

# Car guard
# Stop car when hitting obstacle or when user presses button 4
guard = CarGuard()
guard.start()

# Manual control using keyboard
getch = _Getch()
print("Use keyboard to control: wasd")
print("Quit: q")
while not gs.exit_signal:
    key = getch()
    if key == "w":
        if gs.speed < 0:
            gs.speed = 0
        else:
            gs.speed = min(cf.MAX_SPEED, gs.speed + 2)
    elif key == "s":
        if gs.speed > 0:
            gs.speed = 0
        else:
            gs.speed = max(-cf.MAX_SPEED, gs.speed - 2)
    elif key == "a":
        if gs.steer > 0:
            gs.steer = 0
        else:
            gs.steer = max(cf.MIN_ANGLE, gs.steer - 5)
    elif key == "d":
        if gs.steer < 0:
            gs.steer = 0
        else:
            gs.steer = min(cf.MAX_ANGLE, gs.steer + 5)
    elif key == "i": # Remove emergency stop state
        gs.emergency_stop = False
    elif key == "q":
        gs.exit_signal = True
        exit(0)

    # Decrease speed and angle over time
    gs.speed *= 0.95
    gs.steer *= 0.95

    print("Speed: {}  Steer: {}".format(gs.speed, gs.steer))

mc.join()
button_reader.join()
guard.join()
