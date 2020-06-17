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
        count = 0
        # echopin이 High 상태로 변할때까지 기다림
        while GPIO.input(self.__echopin) == GPIO.LOW:
            count += 1
            startTime = time.time()
            if count > 10000:
                return self.read()
        # echopin이 Low 상태로 변할때까지 기다림
        count = 0
        while GPIO.input(self.__echopin) == GPIO.HIGH:
            count +=1
            stopTime = time.time()
            if count > 10000:
                return self.read()
        # 거리 계산(단위: cm)
        during = stopTime - startTime
        dist = during * (340 / 2) * 100
        return dist

#########################################################





