# ====== Camera ======
OPENNI_PATH = "/home/ubuntu/superfast/libs/OpenNI"

# ====== Motors ======
MOTOR_FREQ = 97 # Provided by FPT

# /* Duty cycle
#     PCA9685 has 12 bits resolution: 4096
#     Neutral Duty 15% 
#     Max_Forward 20%
#     Max_Reverse 10%
    
#     Servo EMAX at 50Hz
#     0           3.6%
#     180        12.8%
# */
THROTTLE_MAX_REVERSE   = 410
THROTTLE_NEUTRAL       = 614 
THROTTLE_MAX_FORWARD   = 819

STEERING_MAX_RIGHT     = 410 
STEERING_MAX_LEFT      = 819

# The THROTTLE is plugged into the following PWM channel
THROTTLE_CHANNEL        = 1
#  The Steering Servo is plugged into the following PWM channel
STEERING_CHANNEL        = 0

MIN_ANGLE = -60 # 10 * maxLeft angle(20 degree) = -200, mul 10 to smooth control
MAX_ANGLE = 60  # 10 * maxRight angle

MAX_SPEED = 20

MIN_SERVO = 0
MAX_SERVO = 180


# ====== LCD ======
# LCD Address
LCD_ADDRESS = 0x22

# ====== Buttons ======
GPIO_BUTTON_1 = 395
GPIO_BUTTON_2 = 393
GPIO_BUTTON_3 = 394
GPIO_BUTTON_4 = 392

GPIO_BUTTON_SS1 = 398
GPIO_BUTTON_SS2 = 396