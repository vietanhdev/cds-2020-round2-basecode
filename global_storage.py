import queue

# Set this to True to exit
exit_signal = False

# Images from camera
rgb_frames = queue.Queue(5)
depth_frames = queue.Queue(5)

# Motor states
pause = False
speed = 0
steer = 0

# Buttons
button_1 = False
button_2 = False
button_3 = False
button_4 = False
button_ss1 = False
button_ss2 = False