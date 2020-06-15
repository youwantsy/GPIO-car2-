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

class Publisher:
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

    def connect(self):
        print("connect")
        thread = threading.Thread(target=self.__run, daemon=True)
        thread.start()

    def disconnect(self):
        self.client.disconnect()

    def __on_connect(self, client, userdata, flags, rc):
        print("ImageMqttClient mqtt broker connected")

    def __on_disconnect(self, client, userdata, rc):
        print("ImageMqttClient mqtt broker disconnected")

    def sendBase64(self, frame):
        if self.client.is_connected() is False: # jpg -> cv2.imeconde ->  base64.b64encode
            return
        retval, bytes = cv2.imencode('.jpg', frame)
        if not retval:
            print("image encoding fail")
            return
        b64_bytes = base64.b64encode(bytes)
        self.client.publish(self.pubtopic, b64_bytes)
#
if __name__ == "__main__":
    queue = deque()
    pcf8591 = Pcf8591(0x48)
    gas = Gas(pcf8591, ain=2)
    thermister = Thermistor(pcf8591, ain=1)
    tracking = Tracking(32)
    photoresister = Photoresister(pcf8591, ain=0)
    ultra = HcSr04(trigpin=38, echopin=40)
    publisher = Publisher("192.168.3.177", 1883, '/sensor')
    publisher.connect()

    while True:
        queue.append({"Gas":gas.read(), "Thermister":thermister.read(), "Ultrasonic":ultra.read(), "Photoresister":photoresister.read(), "Tracking":tracking.read()})
        print(queue)
        time.sleep(0.5)
        publisher.client.publish(publisher.pubtopic, payload=json.dumps(queue.popleft()))