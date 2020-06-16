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

class Publisher_sensor:
    def __init__(self, brokerIp, brokerPort, pubtopic):
        self.__brokerIp = brokerIp
        self.__brokerPort = brokerPort
        self.pubtopic = pubtopic

    def __run(self):
        self.client = mqtt.Client()
        self.client.on_connect= self.__on_connect
        self.client.on_disconnect = self.__on_disconnect
        self.client.connect(self.__brokerIp, self.__brokerPort)
        self.client.loop_forever()

    def connect(self,gas ,thermister, photoresister, tracking, ultra,queue):
        print("Sconnect")
        thread = threading.Thread(target=self.read_sensor, daemon=True ,args=[gas ,thermister, photoresister, tracking, ultra,queue])
        thread.start()
        thread2 = threading.Thread(target=self.__run, daemon=True)
        thread2.start()
    def disconnect(self):
        self.client.disconnect()

    def __on_connect(self, client, userdata, flags, rc):
        print("SImageMqttClient mqtt broker connected")

    def __on_disconnect(self, client, userdata, rc):
        print("SImageMqttClient mqtt broker disconnected")


    def read_sensor(self,gas ,thermister, photoresister, tracking, ultra, queue):
        while True:
            data = {}
            data.update({"Gas": gas.read()})
            data.update({"Thermister": thermister.read()})
            data.update({"Ultrasonic": ultra.read()})
            data.update({"Photoresister": photoresister.read()})
            data.update({"Tracking": tracking.read()})
            queue.append(data)
            print(queue)
            time.sleep(0.3)
            self.client.publish(self.pubtopic, payload=json.dumps(queue.popleft()))
            time.sleep(0.3)
#
