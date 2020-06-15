from Sg90 import Sg90
from Buzzer import Buzzer
from Lcd1602 import Lcd1602
from Laser import Laser
from RgbLed import RgbLed
from HcSr04 import HcSr04
from Photoresister import Photoresister
from Tracking import Tracking
from Thermistor import Thermistor
from Gas import Gas
from DC_Motor import DC
from Pca9685 import Pca9685
from Pcf8591 import Pcf8591
import time

#######################################
#                 BUS                 #
#######################################
pca9685 = Pca9685()
pcf8591 = Pcf8591(0x48)

#######################################
#               ACTIVE                #
#######################################
# SG90
sg90_camera_height = Sg90(pca9685, 0)           # 5~90도     (default = 12도, 줄어들면 LOWER, 커지면 HIGHER)
sg90_camera_width = Sg90(pca9685, 1)            # 12~170도   (default = 90도, 줄어들면 RIGHT, 커지면 LEFT)
sg90_wheel = Sg90(pca9685, 14)                  # 50~130도   (default = 90도, 줄어들면 LEFT, 커지면 RIGHT)
sg90_ultrasonic = Sg90(pca9685, 15)

# DC
dc_left = DC(11, 12, pca9685)
dc_right = DC(13, 15, pca9685)

# BUZZER
buzzer = Buzzer(35)

# LASER
laser = Laser(37)

# LED
rgbLed = RgbLed(16,18,22)

# LCD
lcd = Lcd1602(0x27)
########################################
#               SENSOR                 #
########################################
# GAS
gas = Gas(pcf8591, ain=2)

# ULTRASONIC
ultrasonic = HcSr04(38,40)

# PHOTORESISTOR
photoresistor = Photoresister(pcf8591,ain=0)

# THERMISTOR
thermistor = Thermistor(pcf8591, ain=1)

# TRACKING
tracking = Tracking(32)

############################################
#                   MAIN                   #
############################################

# while True:
#     ggas = gas.read()
#     distance = ultrasonic.read()
#     photo = photoresistor.read()
#     therm = thermistor.read()
#     track = tracking.read()
#     time.sleep(0.5)
#
#     print("ggas: {}".format(ggas))
#     print("distance: {}".format(distance))
#     print("photo: {}".format(photo))
#     print("therm: {}".format(therm))
#     print("track: {}".format(track))

# DC
channel_left = 5
channel_right = 4

set_speed = 30

dc_right.front(channel_right, set_speed)
dc_left.front(channel_left, set_speed - 3)
time.sleep(3)

# SG90
for i in range(50, 90):
    sg90_camera_height.angle(i)
    sg90_camera_width.angle(i)
    sg90_wheel.angle(i)
    sg90_ultrasonic.angle(i)
    time.sleep(0.1)

for i in range(40):
    sg90_camera_height.angle(90 - i)
    sg90_camera_width.angle(90 - i)
    sg90_wheel.angle(90 - i)
    sg90_ultrasonic.angle(90 - i)
    time.sleep(0.1)

sg90_camera_width.angle(90)
sg90_camera_height.angle(12)
sg90_wheel.angle(90)
sg90_ultrasonic.angle(80)

dc_right.stop()
dc_left.stop()