import RPi.GPIO as GPIO
import time

class Tracking:
    def __init__(self, channel):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(channel, GPIO.IN)
        self.__channel = channel

    def read(self):
        value = GPIO.input(self.__channel)
        # white = 0 / black = 1
        return value

if __name__ == "__main__":
    tracking = Tracking(32)
    while True:
        color = tracking.read()
        print(color)
        time.sleep(0.5)