import queue

# Set this to True to exit
exit_signal = False

# Images from camera
rgb_frames = queue.Queue(5)
depth_frames = queue.Queue(5)

# Global variables (shared between python files)
pause = False
speed = 0
steer = 0