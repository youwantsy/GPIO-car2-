import threading
import cv2
import paho.mqtt.client as mqtt
import base64
from Mqtt.Publisher_camera import Publisher_camera
from Mqtt.Publisher_sensor import Publisher_sensor
from HcSr04 import HcSr04
from Photoresister import Photoresister
from Tracking import Tracking
from Thermistor import Thermistor
from Gas import Gas

from Pcf8591 import Pcf8591
from collections import deque
import time
import json

class Sensing_Rover:
    def __init__(self):
        # super().__init__(target=read_sensor)
        pass

    def read_sensor(self,gas ,thermister, photoresister, tracking, ultra,queue):
        publisher_sensor.read_sensor(gas ,thermister, photoresister, tracking, ultra,queue)

    def send(self):
        pass

    def run_dc(self):
        pass

    def run_sg(self):
        pass

    def run_laser(self):
        pass

    def run_led(self):
        pass

    def run_buzzer(self):
        pass

    def run_lcd(self):
        pass

    def read_camera(self, video):
        publiser_camera.read_camera(video)

if __name__ == "__main__":
    sensing_Rover = Sensing_Rover()
    pcf8591 = Pcf8591(0x48)
    gas = Gas(pcf8591, ain=2)
    thermister = Thermistor(pcf8591, ain=1)
    tracking = Tracking(32)
    photoresister = Photoresister(pcf8591, ain=0)
    ultra = HcSr04(trigpin=38, echopin=40)
    queue = deque()
    video = cv2.VideoCapture(0)
    video.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    video.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    publiser_camera = Publisher_camera("192.168.3.177", 1883, "/camerapub")
    publiser_camera.connect()
    publisher_sensor = Publisher_sensor("192.168.3.177", 1883, "/sensor")
    publisher_sensor.connect()

    thread_sensor = threading.Thread(target=sensing_Rover.read_sensor(gas ,thermister, photoresister, tracking, ultra,queue))
    thread_camera = threading.Thread(target=sensing_Rover.read_camera(video))

    #thread_sensor.start()
    thread_camera.start()

    while True:
            pass
