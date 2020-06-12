import RPi.GPIO as GPIO
import time

class Laser:
    ON = "on"
    OFF = "off"

    def __init__(self, channel):
        self.__channel = channel
        self.__state = Laser.OFF
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(channel,GPIO.OUT, initial = GPIO.HIGH)

    def on(self):
        self.state = Laser.ON
        GPIO.output(self.__channel, GPIO.LOW)

    def off(self):
        self.state = Laser.OFF
        GPIO.output(self.__channel, GPIO.HIGH)

if __name__ == "__main__":
    try:
        laser = Laser(37)
        while True:
            laser.off()
            print("laser off")
            time.sleep(3)
            laser.on()
            print("laser on")
            time.sleep(3)
    except KeyboardInterrupt:
        print()
    finally:
        laser.off()
        print("program exit")