import base64
import paho.mqtt.client as mqtt
import threading
import numpy as np
import queue

class Subscriber_order:
    def __init__(self,brokerIp, brokerPort, subtopic):
        self.__brokerIp = brokerIp
        self.__brokerPort = brokerPort
        self.__subtopic = subtopic

    def connect(self):
        thread = threading.Thread(target=self.__run)
        thread.start()

    def __run(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.__on_connect
        self.client.on_disconnect = self.__on_disconnect
        self.client.connect(self.__brokerIp, self.__brokerPort)
        self.client.loop_forever()

    def __on_connect(self, client, userdata, flags, rc):
        print("Subscriber_order mqtt broker connected")
        self.on_message = self.__on_message
        self.client.subscribe(self.__subtopic)

    def __on_disconnect(self):
        print("Subscriber_order mqtt broker disconnected")

    def __on_message(self, client, userdata, message):
        print("message")
        data = str(message.payload, encoding="utf-8")
        print(data)

    def disconnect(self):
        self.client.disconnect()

if __name__ == "__main__":
    subscriber_order = Subscriber_order("192.168.3.177", 1883, "#")
    subscriber_order.connect()