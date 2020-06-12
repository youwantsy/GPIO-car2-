import RPi.GPIO as GPIO
import time

class HcSr04:
    def __init__(self, trigpin=None, echopin=None):
        self.__trigpin = trigpin
        self.__echopin = echopin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(trigpin, GPIO.OUT)
        GPIO.setup(echopin, GPIO.IN)

    def read(self):
        # trigger pin High, 10마이크로초 동안 유지
        GPIO.output(self.__trigpin, GPIO.HIGH)
        time.sleep(0.00001)

        # trigger pin Low(초음파 발생)
        GPIO.output(self.__trigpin, GPIO.LOW)

        startTime = time.time()
        stopTime = time.time()

        # echopin이 High 상태로 변할때까지 기다림
        while GPIO.input(self.__echopin) == GPIO.LOW:
            startTime = time.time()

        # echopin이 Low 상태로 변할때까지 기다림
        while GPIO.input(self.__echopin) == GPIO.HIGH:
            stopTime = time.time()

        # 거리 계산(단위: cm)
        during = stopTime - startTime
        dist = during * (340 / 2) * 100

        return dist

#########################################################
if __name__ == "__main__":
    try:
        sensor = HcSr04(trigpin=38, echopin=40)
        while True:
            distance = sensor.read()
            print("거리: {}".format(distance))
            time.sleep(0.3)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
        print("Program Exit")




