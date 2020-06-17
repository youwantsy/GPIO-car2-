import threading
import cv2
import paho.mqtt.client as mqtt
import base64
import RPi.GPIO as GPIO
from Mqtt.Publisher_camera import Publisher_camera
from Mqtt.Publisher_sensor import Publisher_sensor
from Mqtt.Subscriber_order import Subscriber_order
from HcSr04 import HcSr04
from Photoresister import Photoresister
from Tracking import Tracking
from Thermistor import Thermistor
from Gas import Gas
from RgbLed import RgbLed
from Pcf8591 import Pcf8591
from collections import deque
from Buzzer import Buzzer
from Laser import Laser
from Lcd1602 import Lcd1602
import queue
import time
import json

class Sensing_Rover():
    def __init__(self):
        pass

    def __run(self):
        pass

    def read_sensor(self,gas ,thermister, photoresister, tracking, queue,):
        publisher_sensor.read_sensor(gas ,thermister, photoresister, tracking, queue)

    def send(self):
        pass

    def run_dc(self):
        pass

    def run_sg(self):
        pass

    def run_laser(self, orderdata):
        if orderdata == "ENABLE":
            laser.on()
        if orderdata == "DISABLE":
            laser.off()

    def run_led(self, orderdata):
        if orderdata == "R":
            rgbLed.red()
        if orderdata == "G":
            rgbLed.green()
        if orderdata == "B":
            rgbLed.blue()
        if orderdata == "N":
            rgbLed.off()

    def run_buzzer(self, orderdata):
        if orderdata == "ON":
            buzzer.on()
        if orderdata == "OFF":
            buzzer.off()


    def run_lcd(self, orderdata):
        if orderdata == "TURNON":
            lcd.write(0,0,"HI HI HI")
            lcd.write(0,1,"BYE BYE BYE")
        if orderdata == "TURNOFF":
            lcd.clear()

    def read_camera(self, video):
        publiser_camera.read_camera(video)

if __name__ == "__main__":
    GPIO.cleanup()
    sensing_Rover = Sensing_Rover()

    pcf8591 = Pcf8591(0x48)
    gas = Gas(pcf8591, ain=2)
    thermister = Thermistor(pcf8591, ain=1)
    tracking = Tracking(32)
    photoresister = Photoresister(pcf8591, ain=0)
    ultra = HcSr04(trigpin=38, echopin=40)
    queue = deque()
    rgbLed = RgbLed(16,18,22)
    buzzer = Buzzer(35)
    laser = Laser(37)
    lcd = Lcd1602(0x27)

    publiser_camera = Publisher_camera("192.168.3.177", 1883, "/camerapub")
    publiser_camera.connect()

    publisher_sensor = Publisher_sensor("192.168.3.177", 1883, "/sensor", "/ultra")
    publisher_sensor.connect(gas ,thermister, photoresister, tracking, ultra, queue)

    subscriber_order = Subscriber_order("192.168.3.177", 1883, "/order/#")
    subscriber_order.connect()

    while True:
        if len(subscriber_order.data) != 0:
            orderdata = subscriber_order.data.popleft()

            k,v = orderdata.popitem()
            print(k)
            print(v)
            if  k == '/order/buzzer':
                sensing_Rover.run_buzzer(v)
            elif  k == '/order/led':
                sensing_Rover.run_led(v)
            elif  k == '/order/laser':
                sensing_Rover.run_laser(v)
            elif  k == '/order/lcd':
                sensing_Rover.run_lcd(v)