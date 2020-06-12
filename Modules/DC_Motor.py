import time
from Modules.Pca9685 import Pca9685
import RPi.GPIO as GPIO

class DC:
    def __init__(self, inA, inB, pca9685, frequency = 50):
        self.__inA = inA
        self.__inB = inB
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(inB, GPIO.OUT, initial = GPIO.HIGH)
        GPIO.setup(inA, GPIO.OUT, initial = GPIO.HIGH)
        self.__pca9685 = pca9685
        pca9685.frequency = frequency

    def __speed(self, speed): # 300언저리 min (cm/s) 최대속도 81.64cm/s
        speed = speed*50
        return speed

    def stop(self):
        GPIO.output(self.__inA, GPIO.LOW)
        GPIO.output(self.__inB, GPIO.LOW)

    def front(self,channel, speed):
        GPIO.output(self.__inA, GPIO.LOW)
        GPIO.output(self.__inB, GPIO.HIGH)
        self.__pca9685.write(channel, self.__speed(speed))

    def back(self, channel, speed):
        GPIO.output(self.__inA, GPIO.HIGH)
        GPIO.output(self.__inB, GPIO.LOW)
        self.__pca9685.write(channel, self.__speed(speed))


if __name__ =="__main__":
    pca9685 = Pca9685()
    dc_left = DC(11, 12, pca9685)
    dc_right = DC(13, 15, pca9685)

    channel_left = 5
    channel_right = 4

    # for i in range(4000):
    #     dc_left.front(channel_left,  i)
    #     dc_right.front(channel_right, i)
    #     time.sleep(0.001)
    set_speed = 30
    # time.sleep(3)
    dc_left.stop()
    dc_right.stop()
    # time.sleep(1)
    dc_right.front(channel_right, set_speed)
    dc_left.front(channel_left, set_speed - 3)
    time.sleep(5)
    dc_right.back(channel_right, set_speed)
    dc_left.back(channel_left, set_speed - 8)
    time.sleep(5)
    dc_left.stop()
    dc_right.stop()

