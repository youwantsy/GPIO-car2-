import RPi.GPIO as GPIO
import time

class RgbLed:
    RED ="red"
    GREEN = "green"
    BLUE = "blue"

    def __init__(self, redPin=None, greenPin=None, bluePin=None):
        self.__redPin = redPin
        self.__greenPin = greenPin
        self.__bluePin = bluePin
        self.state = None
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        if redPin is not None:
            GPIO.setup(redPin, GPIO.OUT, initial=GPIO.HIGH)
        if greenPin is not None:
            GPIO.setup(greenPin, GPIO.OUT, initial=GPIO.HIGH)
        if bluePin is not None:
            GPIO.setup(bluePin, GPIO.OUT, initial=GPIO.HIGH)

    def red(self):
        self.state = RgbLed.RED
        if self.__redPin is not None:
            GPIO.output(self.__redPin, GPIO.LOW)
        if self.__greenPin is not None:
            GPIO.output(self.__greenPin, GPIO.HIGH)
        if self.__bluePin is not None:
            GPIO.output(self.__bluePin, GPIO.HIGH)

    def green(self):
        self.state = RgbLed.GREEN
        if self.__redPin is not None:
            GPIO.output(self.__redPin, GPIO.HIGH)
        if self.__greenPin is not None:
            GPIO.output(self.__greenPin, GPIO.LOW)
        if self.__bluePin is not None:
            GPIO.output(self.__bluePin, GPIO.HIGH)

    def blue(self):
        self.state = RgbLed.BLUE
        if self.__redPin is not None:
            GPIO.output(self.__redPin, GPIO.HIGH)
        if self.__greenPin is not None:
            GPIO.output(self.__greenPin, GPIO.HIGH)
        if self.__bluePin is not None:
            GPIO.output(self.__bluePin, GPIO.LOW)

    def off(self):
        self.state = None
        if self.__redPin is not None:
            GPIO.output(self.__redPin, GPIO.HIGH)
        if self.__greenPin is not None:
            GPIO.output(self.__greenPin, GPIO.HIGH)
        if self.__bluePin is not None:
            GPIO.output(self.__bluePin, GPIO.HIGH)

if __name__ =="__main__":
    rgbLed = RgbLed(16, 18,22)

    rgbLed.red()
    time.sleep(2)
    rgbLed.off()
    time.sleep(1)

    rgbLed.green()
    time.sleep(2)
    rgbLed.off()
    time.sleep(1)

    rgbLed.blue()
    time.sleep(2)
    rgbLed.off()
    time.sleep(1)

    rgbLed.red()
    rgbLed.green()
    time.sleep(2)
    rgbLed.off()
    time.sleep(1)

    rgbLed.red()
    rgbLed.blue()
    time.sleep(2)
    rgbLed.off()
    time.sleep(1)

    rgbLed.green()
    rgbLed.blue()
    time.sleep(2)
    rgbLed.off()
    time.sleep(1)

    rgbLed.red()
    rgbLed.green()
    rgbLed.blue()
    time.sleep(2)
    rgbLed.off()
    time.sleep(1)