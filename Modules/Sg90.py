from Modules.Pca9685 import Pca9685
import time

class Sg90:
    def __init__(self, pca9685, channel, frequency=50):
        self.__pca9685 = pca9685
        self.__channel = channel
        pca9685.frequency = frequency

    def __map(self, angle):
        return int(164 + angle*((553-164)/180))

    def angle(self, angle):
        self.__pca9685.write(self.__channel, self.__map(angle))

if __name__ == "__main__":
    pca9685 = Pca9685()
    sg90_camera_height = Sg90(pca9685, 0)           # 5~90도     (default = 12도, 줄어들면 LOWER, 커지면 HIGHER)
    sg90_camera_width = Sg90(pca9685, 1)            # 12~170도   (default = 90도, 줄어들면 RIGHT, 커지면 LEFT)
    sg90_wheel = Sg90(pca9685, 14)                  # 50~130도   (default = 90도, 줄어들면 LEFT, 커지면 RIGHT)
    sg90_ultrasonic = Sg90(pca9685, 15)             # 40~120도   (default = 80도, 줄어들면 RIGHT, 커지면 LEFT)

    for i in range(50,90):
        sg90_camera_height.angle(i)
        sg90_camera_width.angle(i)
        sg90_wheel.angle(i)
        sg90_ultrasonic.angle(i)
        time.sleep(0.1)

    for i in range(40):
        sg90_camera_height.angle(90-i)
        sg90_camera_width.angle(90-i)
        sg90_wheel.angle(90-i)
        sg90_ultrasonic.angle(90-i)
        time.sleep(0.1)

    sg90_camera_width.angle(90)
    sg90_camera_height.angle(12)
    sg90_wheel.angle(90)
    sg90_ultrasonic.angle(80)
