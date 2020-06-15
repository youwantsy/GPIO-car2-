import threading
import cv2
import paho.mqtt.client as mqtt
import base64
import json


#v = cv2.VideoCapture(0)
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
        self.client.publish(self.pubtopic , b64_bytes)
#
if __name__ == "__main__":
    video = cv2.VideoCapture(0)
    video.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    video.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    publiser = Publisher("192.168.3.177", 1883, '/camerapub')
    publiser.connect()

    while True:
        if video.isOpened():
            retval, data = video.read()
            if not retval:
                print("read fail")
                break
            publiser.sendBase64(data)
        else:
            break

    video.release()
    publiser.disconnect()
    print("Program exit")