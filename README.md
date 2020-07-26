# Digital Race - Cuộc đua số - ROUND 2

This code was written based on the original code from [FPT Dira platform](https://github.com/fpt-corp/DiRa). In this repository, we target Jetson TX2 with Traxxas car model.

## Requirements:
- Hardware: DIRA platform - FPT
- Python 3.6

## I2C
- List I2C: `sudo i2cdetect -y -r 1`.

## Camera
- Library: `primesense`.
- Install:
```
sudo pip3 install primesense
```

## Motors:
- Library: https://github.com/adafruit/Adafruit_Python_PCA9685
- Document: phtts://readthedocs.org/projects/adafruit-circuitpython-pca9685/downloads/pdf/latest/
```
sudo pip3 install adafruit-pca9685
```

##  GPIO: 
- https://devtalk.nvidia.com/default/topic/1030443/jetson-tx2/using-gpio-on-nvidia-jetson-tx2/
- Using library: https://github.com/vitiral/gpio.git
- GPIO without root: https://jkjung-avt.github.io/gpio-non-root/. (`dependencies/non_root_gpio/`)
```
sudo pip3 install gpio
cd dependencies/non_root_gpio/
sh setup_gpio.sh
```

## LCD:
- Library: smbus
```
sudo pip3 install smbus
```
- Update LCD I2C address in `config.py` -> `LCD_ADDRESS`.

## Gyro
https://github.com/RTIMULib/RTIMULib2.git
```
cd dependencies/RTIMULib2/Linux/python
python3 setup.py build
python3 setup.py install
```

## Remote control using Android smartphone

- Download and use this app: https://play.google.com/store/apps/details?id=com.denods.udpjoystick&hl=vi
- Enter ip address to Jetson and enter port 12345.
- Use y axis of left joystick to control speed and x axis of right joystick to control steering angle.
- **Special functions:** move left joystick to y = 0 and right joystick to special position to activate special functions:
    + Top - right: Emergency stop.
    + Top - left: Remove emergency stop flag.
    + Bottom - right: Start video recording.
    + Bottom - left: Stop video recording.
