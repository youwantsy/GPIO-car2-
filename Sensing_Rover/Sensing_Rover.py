import threading
import cv2
import paho.mqtt.client as mqtt
import base64

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
        pass

    def read_sensor(self):
        pass

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
