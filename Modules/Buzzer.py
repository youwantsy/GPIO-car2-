import RPi.GPIO as GPIO
import time

class Buzzer:
    ON = "on"
    OFF = "off"

    def __init__(self, channel):
        self.__channel = channel
        self.__state = Buzzer.OFF
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(channel,GPIO.OUT, initial = GPIO.HIGH)

    def on(self):
        self.state = Buzzer.ON
        GPIO.output(self.__channel, GPIO.LOW)

    def off(self):
        self.state = Buzzer.OFF
        GPIO.output(self.__channel, GPIO.HIGH)

if __name__ == "__main__":
    try:
        buzzer = Buzzer(35)
        while True:
            buzzer.on()
            time.sleep(0.5)
            buzzer.off()
            time.sleep(0.5)
    except KeyboardInterrupt:
        print()
    finally:
        buzzer.off()
        print("program exit")